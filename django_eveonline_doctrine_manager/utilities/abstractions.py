class EveSkillList():
    def __init__(self):
        self.skill_list = []
        self.skill_key = set()
    
    def add_skill(self, skill):
        for level in range(1, int(skill['level'])+1):
            skill_to_add = f"{skill['name']} {level}"
            if skill_to_add in self.skill_key:
                continue
            self.skill_list.append(skill_to_add)
            self.skill_key.add(skill_to_add)

