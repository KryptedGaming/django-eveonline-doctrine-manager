from django.db import models
from django.apps import apps
from django_eveonline_connector.utilities.static.universe import resolve_type_name_to_type_id, get_type_id_prerq_skill_ids, get_prerequisite_skills, resolve_type_id_to_type_name
from django_eveonline_doctrine_manager.utilities.abstractions import EveSkillList
from django.core.validators import MaxValueValidator, MinValueValidator
import json, logging, re

logger = logging.getLogger(__name__)

"""
Helper functions
"""


def get_skill_names_from_static_dump():
    import django_eveonline_doctrine_manager
    import os
    pth = os.path.dirname(django_eveonline_doctrine_manager.__file__)
    with open(pth + '/export/skills.json', 'r') as fp:
        skills = json.load(fp)

    return [ (skill, skill) for skill in skills.keys()]


"""
Core models
These are the main data models for the doctrine manager
"""


class EveDoctrine(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField("EveDoctrineManagerTag", blank=True)
    category = models.ForeignKey(
        "EveDoctrineCategory", on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def fittings(self):
        return EveFitting.objects.filter(doctrines__in=[self])
    
    @property
    def skill_plans(self):
        return EveSkillPlan.objects.filter(doctrines__in=[self])

    def __str__(self):
        return self.name

class EveDoctrineManagerBaseObject(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField("EveDoctrineManagerTag", blank=True)
    doctrines = models.ManyToManyField("EveDoctrine", blank=True)
    roles = models.ManyToManyField("EveDoctrineRole", blank=True)
    
class EveFitting(EveDoctrineManagerBaseObject):
    fitting = models.TextField()  # eft format
    # eve static info
    ship_id = models.IntegerField(editable=False, blank=True, null=True)
    # associations 
    refit_of = models.ForeignKey("EveFitting", null=True, default=None, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.ship_id = self.get_ship_id()
        super(EveFitting, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def mod_array(self, mod):
        resolution = resolve_type_name_to_type_id(mod)
        return {
            'name': mod,
            'type_id': resolution
        }

    def get_ship_name(self):
         fitting = self.fitting.splitlines()
         line = fitting[0]
         return line[1:-1].split(',')[0].strip()
        
    def get_ship_id(self):
        return self.mod_array(self.get_ship_name())['type_id']

    def get_required_skills(self):
        fitting = self.parse_fitting()
        exclude_keys = ['name']
        top_level_skills = []

        for key in fitting:
            
            if key in exclude_keys:
                logger.debug(f"skipping fitting key {key}")
                continue

            module_list = fitting[str(key)]
            unique_modules = set()
            for module in module_list:
                unique_modules.add(module['type_id'])

            for module in unique_modules:
                logger.debug(f"Resolving skills for {module}")
                top_level_skills += get_type_id_prerq_skill_ids(module)
            
            skill_list = EveSkillList()
            for skill in top_level_skills:
                for prerq_skill in reversed(get_prerequisite_skills([skill])):
                    skill_list.add_skill(prerq_skill)

        return skill_list  

    def parse_fitting(self):
        fit = {'name':'','ship':'','high':[],'mid':[],'low':[],'rig':[], 'drones':[], 'cargo':[]}
        item = ['name', 'low','mid','high','rig','drones', 'cargo']
        fitting = self.fitting.splitlines()
        fitting.reverse()
        case = 0
        while len(fitting) > 1:
            if (fitting[-1] == '' or fitting[-1].isspace()):
                line = fitting.pop()
                case += 1
                while(fitting[-1].isspace() or fitting[-1] == ""):
                    excess = fitting.pop()
                continue
            else:
                line = fitting.pop()

            if 'Empty' in line:
                continue
            # process case 
            if (case == 0):
                fit['name'] = line[1:-1].split(',')[1].strip()
                fit['ship'] = [self.mod_array(line[1:-1].split(',')[0].strip())]
            elif (case == 1):
                # lowslots
                fit[item[case]].append(self.mod_array(line.split(',')[0]))
            elif (case == 2):
                # midslots
                fit[item[case]].append(self.mod_array(line.split(',')[0]))
            elif (case == 3):
                # highslots
                fit[item[case]].append(self.mod_array(line.split(',')[0]))
            elif (case == 4):
                # rigs 
                fit[item[case]].append(self.mod_array(line.split(',')[0]))
            elif (case == 5):
                # drones 
                if (line.split(",")[0].split(" ")[-1][0] == "x" and line.split(",")[0].split(" ")[-1][1].isnumeric()):
                        for amount in range(0,int(line.split(',')[0].split(" ")[-1][1:])):
                            fit[item[case]].append(self.mod_array(line.split(',')[0][:-3]))
                else:
                    fit[item[case]].append(self.mod_array(line.split(',')[0]))
            elif (case == 6):
                # cargo 
                if (line.split(",")[0].split(" ")[-1][0] == "x" and line.split(",")[0].split(" ")[-1][1].isnumeric()):
                        for amount in range(0,int(line.split(',')[0].split(" ")[-1][1:])):
                            fit[item[case]].append(self.mod_array(line.split(',')[0][:-3]))
                else:
                    fit[item[case]].append(self.mod_array(line.split(',')[0]))
        return fit

class EveSkillPlan(EveDoctrineManagerBaseObject):
    def __str__(self):
        return self.name    

"""
Grouping models
Used to group fittings and doctrines for users and clarity.
"""
class EveRequiredSkill(models.Model):
    name = models.CharField(
        max_length=64, choices=get_skill_names_from_static_dump())
    level = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    skill_for = models.ForeignKey("EveDoctrineManagerBaseObject", on_delete=models.CASCADE)

class EveDoctrineRole(models.Model):
    name = models.CharField(max_length=128)
    icon = models.URLField()

    def __str__(self):
        return self.name

class EveDoctrineCategory(models.Model):
    name = models.CharField(max_length=128)
    icon = models.URLField()

    def __str__(self):
        return self.name

class EveDoctrineManagerTag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


