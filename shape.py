descriptions = [
    ["linear", "linear"],
    ["trigonal planar", "bent", "linear"],
    ["tetrahedral", "trigonal pyramidal", "bent", "linear"],
    ["trigonal bipyramidal", "see-saw", "t-shape", "linear"],
    ["octahedral", "square pyramidal", "square planar", "t-shape", "linear"]
]

bondAngles = [
    ["180", "no angle"],
    ["120", "120", "no angle"],
    ["109.5", "<109.5", "<109.5", "no angle"],
    ["120 equatorial, 90 axial", "120 equatorial, 90 axial", "90", "180"],
    ["90", "<90", "90", "<90", "180"]
]

def getVSEPRDescription(surrounding, lonePair):
    try:
        return f"""
Electron geometry: {descriptions[surrounding+lonePair - 2][0]}
Molecular geometry: {descriptions[surrounding+lonePair - 2][lonePair]}
Bond angle: {bondAngles[surrounding + lonePair - 2][lonePair]}
"""
    except IndexError:
        return "Invalid formula set"
