art_departments = ['Irish Art', 'Contemporary Ink Art', 'Contemporary Art', 'Modern & Post-War British Art',
                   'British Paintings 1550-1850', 'Old Master Paintings', '19th Century European Paintings',
                   'American Art', 'Canadian Art', 'Impressionist & Modern Art',
                   'Victorian, Pre-Raphaelite & British Impressionist Art', 'British Watercolours & Drawings 1550-1850',
                   'Old Master Drawings']

design_departments = ['American Furniture, Decorative Art & Folk Art', 'European Ceramics', '20th Century Design',
                      'English Furniture', 'French & Continental Furniture', '19th Century Furniture & Sculpture',
                      'European Sculpture & Works of Art']


def category_from_deps_list(deps_list):
    votes = {'art': 0, 'design': 0}

    for dep in deps_list:
        if dep in art_departments:
            votes['art'] += 1
        if dep in design_departments:
            votes['design'] += 1

    if votes['art'] > votes['design']:
        return 'art'
    elif votes['art'] == votes['design']:
        return None
    else:
        return 'design'
