def negotiate_price(base_price, disease_name):
    """
    Determines final price based on AI-detected quality.
    Grade 1: +5% Bonus (Premium)
    Grade 2: Base Price
    Grade 3: -20% Penalty (Animal Feed)
    """
    if disease_name == "Healthy":
        grade = 1
        bonus = 0.05
        explanation = "Grade 1: Premium quality detected. You earned a 5% bonus!"
    elif disease_name in ["Common Rust", "Gray Leaf Spot"]:
        grade = 2
        bonus = 0.0
        explanation = "Grade 2: Standard quality. Accepted at market base price."
    else:
        grade = 3
        bonus = -0.20
        explanation = "Grade 3: Quality issues detected. Recommended for animal feed at -20% discount."

    final_price = base_price * (1 + bonus)
    return grade, round(final_price, 2), explanation