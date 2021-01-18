import random
from flask_restful import Resource, reqparse
minA = 1000
maxA = 9999
minB = 100
maxB = 9999
minC = 2
maxC = 9


class ks(Resource):
    """
    Author: ldqLDQ
    功能: 获取一用户已发布的自习列表
    """
    def get(self):
        def newPlus():
            A = random.randint(minA,maxA)
            B = random.randint(minB,maxB)
            S = A+B
            return str(A)+" + "+str(B)
        def newMinus():
            A = random.randint(minA,maxA)
            B = random.randint(minB,A)
            S = A-B
            return str(A)+" - "+str(B)
        def newMulti():
            A0 = random.randint(minA,maxA)
            B = random.randint(minC,maxC)
            A = int(A0/B)
            S = A*B
            return str(A)+" × "+str(B)
        def newDivi():
            A = random.randint(minA,maxA)
            B = random.randint(minC,maxC)
            #S = A+B
            return str(A)+" ÷ "+str(B)

        s = []
        s.append(newPlus())
        s.append(newMinus())
        s.append(newMulti())
        s.append(newDivi())
        random.shuffle(s)
        r = {1:s[0], 2:s[1], 3:s[2], 4:s[3]}
        return r