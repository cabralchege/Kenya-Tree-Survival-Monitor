def calculate_survival_rate(planted, alive):
    """Calculate survival percentage"""
    if planted == 0:
        return 0
    return round((alive / planted) * 100, 2)

def get_survival_by_species(db_connection):
    """Get survival rates grouped by species"""
    query = """
    SELECT 
        p.species,
        SUM(p.quantity) as total_planted,
        COALESCE(SUM(s.alive_count), 0) as total_alive,
        calculate_survival_rate(total_planted, total_alive) as survival_rate
    FROM plantings p
    LEFT JOIN survival_checks s ON p.id = s.planting_id
    GROUP BY p.species
    """
    return db_connection.execute(query).fetchall()

def get_survival_trend(db_connection, months=6):
    """Get survival trend over time"""
    # Returns data for time-series chart
    pass

def predict_survival_ml(species, location, season):
    """AI prediction for expected survival rate"""
    # ML model prediction logic
    # Returns: predicted_rate, confidence_score
    pass