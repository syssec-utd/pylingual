def get_string_polyglot_attack(self, obj):
    """
        Return a polyglot attack containing the original object
        """
    return self.polyglot_attacks[random.choice(self.config.techniques)] % obj