

def prediction(carat , cut , color , clarity , depth , table , x , y , z):

    if (
        carat and cut and color and clarity and depth and table and x and y and z
    ):

        return "Approved"
    else:

        return "Rejected"
