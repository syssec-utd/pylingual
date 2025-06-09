def winner(self):
    """Returns the team ID of the winning team. Returns NaN if a tie."""
    hmScore = self.home_score()
    awScore = self.away_score()
    if hmScore > awScore:
        return self.home()
    elif hmScore < awScore:
        return self.away()
    else:
        return None