art_departments = {
    66: "19th century European Art",
    3: "American Art",
    101: "British Art on Paper (1600-1850)",
    29: "Impressionist & Modern Art",
    99: "Modern British & Irish Art",
    69: "Old Master Drawings",
    70: "Old Master Paintings",
    74: "Post-War & Contemporary Art",
    96: "Scottish Art",
    50: "Sporting & Wildlife Art",
    100: "Victorian, Pre-Raphaelite & British Impressionist Art"
}

design_departments = {
    68: "19th Century Furniture & Sculpture",
    4: "American Folk Art & Outsider Art",
    5: "American Furniture & Decorative Arts",
    59: "Design",
    111: "Early European Sculpture & Works of Art",
    112: "English Furniture & Works of Art",
    25: "European Ceramics & Glass",
    26: "European Furniture & Works of Art",
    103: "Interiors"
}


def department_name_from_id(id):
    """
    Function helper to translate id to department human name.
    """

    if isinstance(id, str):
        id = int(id)
    if id in art_departments:
        return art_departments[id]
    elif id in design_departments:
        return design_departments[id]
    else:
        return None


def category_from_ids(ids):
    ids = [int(id) if isinstance(id, str) else id for id in ids]

    votes = {'art': 0, 'design': 0}

    for id in ids:
        if id in art_departments:
            votes['art'] += 1
        if id in design_departments:
            votes['design'] += 1

    if votes['art'] > votes['design']:
        return 'art'
    elif votes['art'] == votes['design']:
        return None
    else:
        return 'design'
