from numpy import *

def get_angle(a,b,c,unit):
    a = array(a)
    b = array(b)
    c = array(c)
    if unit == 'Ang':
        ba = (a - b)*0.529177249
        bc = (c - b)*0.529177249
    else:
        ba = a - b
        bc = c - b
    cosine_angle = dot(ba,bc)/(linalg.norm(ba)*linalg.norm(bc))
    angle = arccos(cosine_angle)
    return degrees(angle)

def get_dist(a,b,unit):
    a = array(a)
    b = array(b)
    if unit == 'Ang':
        return linalg.norm((a-b)*0.529177249)
    else:
        return linalg.norm(a-b)

def get_dihedral(p0,p1,p2,p3,unit):
    """Praxeolitic formula
    1 sqrt, 1 cross product"""
    if unit == 'Ang':
        p0 = p0*0.529177249
        p1 = p1*0.529177249
        p2 = p2*0.529177249
        p3 = p3*0.529177249

    b0 = -1.0*(p1 - p0)
    b1 = p2 - p1
    b2 = p3 - p2

    # normalize b1 so that it does not influence magnitude of vector
    # rejections that come next
    b1 /= linalg.norm(b1)

    # vector rejections
    # v = projection of b0 onto plane perpendicular to b1
    #   = b0 minus component that aligns with b1
    # w = projection of b2 onto plane perpendicular to b1
    #   = b2 minus component that aligns with b1
    v = b0 - dot(b0, b1)*b1
    w = b2 - dot(b2, b1)*b1

    # angle between v and w in a plane is the torsion angle
    # v and w may not be normalized but that's fine since tan is y/x
    x = dot(v, w)
    y = dot(cross(b1, v), w)
    return degrees(arctan2(y, x))

    #q1 = subtract(p1,p0) # b - a 
    #q2 = subtract(p2,p1) # c - b 
    #q3 = subtract(p3,p2) # d - c
    #print(q1,q2)

    #q1_x_q2 = cross(q1,q2) 
    #q2_x_q3 = cross(q2,q3)

    #n1 = q1_x_q2/sqrt(dot(q1_x_q2,q1_x_q2)) 
    #n2 = q2_x_q3/sqrt(dot(q2_x_q3,q2_x_q3))

    #u1 = n2
    #u3 = q2/(sqrt(dot(q2,q2))) 
    #u2 = cross(u3,u1)

    #cos_theta = dot(n1,u1)
    #sin_theta = dot(n1,u2)
    ## Calculate theta
    #theta = -atan2(sin_theta,cos_theta)
    ## it is different from atan2 from fortran math.atan2(y,x)
    #theta_deg = degrees(theta)
    #return(theta_deg)
