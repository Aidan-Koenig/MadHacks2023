from pymongo import MongoClient
from flask import Flask, jsonify, request
courseReqs = {'COMP SCI 102': '("MATH 096" or "maybe") and not ("COMP SCI 300" or "COMP SCI 320")',
 'L I S 102': '("MATH 096" or "maybe") and not ("COMP SCI 300" or "COMP SCI 320")',
 'COMP SCI 200': '"QR-A" or "maybe"',
 'COMP SCI 220': '("QR-A" or "maybe") and not "COMP SCI 301"',
 'COMP SCI 240': '"MATH 217" or "MATH 221" or "MATH 275"',
 'MATH 240': '"MATH 217" or "MATH 221" or "MATH 275"',
 'COMP SCI 252': 'True',
 'E C E 252': 'True',
 'COMP SCI 270': 'not "COMP SCI 570"',
 'COMP SCI 298': '"maybe"',
 'COMP SCI 300': '("QR-A" and (("COMP SCI 200" or "COMP SCI 220" or "COMP SCI 302" or "COMP SCI 310" or "COMP SCI 301" or "maybe") or (("E C E 252" or "COMP SCI 252") and "E C E 203")) or "grad") and not "COMP SCI 367"',
 'COMP SCI 304': '"maybe"',
 'COMP SCI 310': '"MATH 222" or "grad" or "maybe"',
 'COMP SCI 319': '"grad"',
 'COMP SCI 320': '"COMP SCI 220" or "COMP SCI 300" or "COMP SCI 319" or "grad" or maybe',
 'COMP SCI 352': '"QR-A" and ("E C E 252" or "COMP SCI 252")',
 'E C E 352': '"QR-A" and ("E C E 252" or "COMP SCI 252")',
 'COMP SCI 354': '("E C E 252" or "COMP SCI 252") and ("COMP SCI 300" or "COMP SCI 302") or "grad" or "maybe"',
 'E C E 354': '("E C E 252" or "COMP SCI 252") and ("COMP SCI 300" or "COMP SCI 302") or "grad" or "maybe"',
 'COMP SCI 368': 'None',
 'COMP SCI 400': '"COMP SCI 300" or "grad" or "maybe"',
 'COMP SCI 402': '"COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" or "COMP SCI 367" or "L I S 102" or "COMP SCI 102" or "grad" or "maybe"',
 'COMP SCI 403': '"maybe"',
 'STAT 403': '"maybe"',
 'COMP SCI 407': '"COMP SCI 300" or "COMP SCI 367" or "grad" or "maybe"',
 'COMP SCI 412': '"MATH 222" and ("MATH 240" or "COMP SCI 240" or "MATH 234") and ("COMP SCI 200" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310") or "grad" or "maybe"',
 'COMP SCI 425': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "grad" or "maybe"',
 'I SY E 425': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "grad" or "maybe"',
 'MATH 425': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "grad" or "maybe"',
 'COMP SCI 435': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "grad" or "maybe"',
 'E C E 435': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "grad" or "maybe"',
 'MATH 435': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "grad" or "maybe"',
 'COMP SCI 471': '("STAT 310" or "MATH 310") and ("STAT 333" or "STAT 340") or "grad" or "maybe"',
 'STAT 471': '("STAT 310" or "MATH 310") and ("STAT 333" or "STAT 340") or "grad" or "maybe"',
 'COMP SCI 475': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "grad" or "maybe"',
 'MATH 475': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "grad" or "maybe"',
 'STAT 475': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "grad" or "maybe"',
 'COMP SCI 502': '"COMP SCI 300" or "COMP SCI 302" or "grad"',
 'CURRIC 502': '"COMP SCI 300" or "COMP SCI 302" or "grad"',
 'COMP SCI 506': '("COMP SCI 367" or "COMP SCI 400") and ("COMP SCI 407" or "COMP SCI 536" or "COMP SCI 537" or "COMP SCI 545" or "COMP SCI 559" or "COMP SCI 564" or "COMP SCI 570" or "COMP SCI 679" or "COMP SCI 552" or "E C E 552") or "grad" or "maybe"',
 'E C E 506': '("COMP SCI 367" or "COMP SCI 400") and ("COMP SCI 407" or "COMP SCI 536" or "COMP SCI 537" or "COMP SCI 545" or "COMP SCI 559" or "COMP SCI 564" or "COMP SCI 570" or "COMP SCI 679" or "COMP SCI 552" or "E C E 552") or "grad" or "maybe"',
 'COMP SCI 513': '"MATH 340" or "MATH 341" or "MATH 375" and ("COMP SCI 200" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310") or "grad" or "maybe"',
 'MATH 513': '"MATH 340" or "MATH 341" or "MATH 375" and ("COMP SCI 200" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310") or "grad" or "maybe"',
 'COMP SCI 514': '("MATH 320" or "MATH 340" or "MATH 341" or "MATH 375") and ("MATH 322" or "MATH 376" or "MATH 421" or "MATH 521") and ("COMP SCI 200" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310") or "grad" or "maybe"',
 'MATH 514': '("MATH 320" or "MATH 340" or "MATH 341" or "MATH 375") and ("MATH 322" or "MATH 376" or "MATH 421" or "MATH 521") and ("COMP SCI 200" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310") or "grad" or "maybe"',
 'COMP SCI 518': '"maybe"',
 'DS 518': '"maybe"',
 'I SY E 518': '"maybe"',
 'COMP SCI 520': '(("MATH 240" or "COMP SCI 240" or "STAT 475" or "COMP SCI 475" or "MATH 475") and ("COMP SCI 367" or "COMP SCI 400")) or "grad" or "maybe"',
 'COMP SCI 524': '"COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" and ("MATH 320" or "MATH 340" or "MATH 341" or "MATH 375") or "grad" or "maybe"',
 'E C E 524': '"COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" and ("MATH 320" or "MATH 340" or "MATH 341" or "MATH 375") or "grad" or "maybe"',
 'I SY E 524': '"COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" and ("MATH 320" or "MATH 340" or "MATH 341" or "MATH 375") or "grad" or "maybe"',
 'COMP SCI 525': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "MATH 443" or "grad" or "maybe"',
 'I SY E 525': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "MATH 443" or "grad" or "maybe"',
 'MATH 525': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "MATH 443" or "grad" or "maybe"',
 'STAT 525': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "MATH 443" or "grad" or "maybe"',
 'COMP SCI 526': '"STAT 525" or "COMP SCI 525" or "I SY E 525" or "MATH 525" and ("COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310") or "grad" or "maybe"',
 'I SY E 526': '"STAT 525" or "COMP SCI 525" or "I SY E 525" or "MATH 525" and ("COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310") or "grad" or "maybe"',
 'COMP SCI 532': '("MATH 234" or "MATH 320" or "MATH 340" or "MATH 341" or "MATH 375") and ("E C E 203" or "COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" or "COMP SCI 320") or "grad" or "maybe"',
 'E C E 532': '("MATH 234" or "MATH 320" or "MATH 340" or "MATH 341" or "MATH 375") and ("E C E 203" or "COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" or "COMP SCI 320") or "grad" or "maybe"',
 'M E 532': '("MATH 234" or "MATH 320" or "MATH 340" or "MATH 341" or "MATH 375") and ("E C E 203" or "COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" or "COMP SCI 320") or "grad" or "maybe"',
 'COMP SCI 533': '("E C E 330" and ("MATH 320" or "MATH 340")) or "grad" or "maybe"',
 'E C E 533': '("E C E 330" and ("MATH 320" or "MATH 340")) or "grad" or "maybe"',
 'COMP SCI 534': '("COMP SCI 300" or "COMP SCI 367") and ("MATH 217" or "MATH 221" or "MATH 275") or "grad" or "maybe"',
 'COMP SCI 536': '("E C E 354" or "COMP SCI 354") and ("COMP SCI 367" or "COMP SCI 400") or "grad" or "maybe"',
 'COMP SCI 537': '("E C E 354" or "COMP SCI 354") and ("COMP SCI 367" or "COMP SCI 400") or "grad" or "maybe"',
 'COMP SCI 538': '("E C E 354" or "COMP SCI 354") and ("COMP SCI 367" or "COMP SCI 400") or "grad" or "maybe"',
 'COMP SCI 539': '"COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" or "grad" or "maybe"',
 'E C E 539': '"COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" or "grad" or "maybe"',
 'M E 539': '"COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" or "grad" or "maybe"',
 'COMP SCI 540': '("COMP SCI 300" or "COMP SCI 320" or "COMP SCI 367") and ("MATH 211" or "MATH 217" or "MATH 221" or "MATH 275") or "grad" or "maybe"',
 'COMP SCI 542': '"COMP SCI 400" or "COMP SCI 320" or "grad" or "maybe"',
 'COMP SCI 544': '"COMP SCI 400" or "COMP SCI 320" or "grad"',
 'COMP SCI 545': '"COMP SCI 536" or "COMP SCI 537" or "COMP SCI 564" or "grad" or "maybe"',
 'COMP SCI 552': '("E C E 352" or "COMP SCI 352" and "E C E 354" or "COMP SCI 354") or "grad"',
 'E C E 552': '("E C E 352" or "COMP SCI 352" and "E C E 354" or "COMP SCI 354") or "grad"',
 'COMP SCI 558': '("COMP SCI 400" or "COMP SCI 367") and "MATH 234" or "grad"',
 'I SY E 558': '("COMP SCI 400" or "COMP SCI 367") and "MATH 234" or "grad"',
 'M E 558': '("COMP SCI 400" or "COMP SCI 367") and "MATH 234" or "grad"',
 'COMP SCI 559': '("MATH 222" or "MATH 276") and ("COMP SCI 367" or "COMP SCI 400") or "grad" or "maybe"',
 'COMP SCI 561': '("MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "M E 532" or "COMP SCI 532" or "E C E 532") and ("E C E 331" or "STAT 309" or "STAT 431" or "MATH 309" or "MATH 431" or "STAT 311" or "STAT 324" or "M E 424" or "STAT 424" or "MATH 531") or "grad" or "maybe"',
 'E C E 561': '("MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" or "M E 532" or "COMP SCI 532" or "E C E 532") and ("E C E 331" or "STAT 309" or "STAT 431" or "MATH 309" or "MATH 431" or "STAT 311" or "STAT 324" or "M E 424" or "STAT 424" or "MATH 531") or "grad" or "maybe"',
 'COMP SCI 564': '("E C E 354" or "COMP SCI 354") and ("COMP SCI 367" or "COMP SCI 400") or "grad" or "maybe"',
 'COMP SCI 565': '"COMP SCI 320" or "COMP SCI 400" or "grad"',
 'COMP SCI 566': '"COMP SCI 400" and ("MATH 320" or "MATH 340" or "MATH 341" or "MATH 375") and ("STAT 309" or "STAT 431" or "MATH 309" or "MATH 431" or "STAT 311" or "STAT 302" or "STAT 324" or "STAT 340" or "STAT 371" or "MATH 331" or "STAT 531") or "grad"',
 'COMP SCI 567': '("MATH 320" or "MATH 340") and ("STAT 511" or "STAT 541" or "POP HLTH 551" or "B M I 551" or "STAT 324" or "STAT 371" or "STAT 571" or "F&W ECOL 571" or "HORT 571") or "grad"',
 'B M I 567': '("MATH 320" or "MATH 340") and ("STAT 511" or "STAT 541" or "POP HLTH 551" or "B M I 551" or "STAT 324" or "STAT 371" or "STAT 571" or "F&W ECOL 571" or "HORT 571") or "grad"',
 'COMP SCI 570': '("COMP SCI 200" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" or "COMP SCI 367" or "L I S 102" or "COMP SCI 102" or "grad" or "maybe") and not "COMP SCI 270"',
 'COMP SCI 571': '"COMP SCI 400"',
 'COMP SCI 576': '("COMP SCI 320" or "COMP SCI 400") and "MATH 222" or "grad" or "maybe"',
 'B M I 576': '("COMP SCI 320" or "COMP SCI 400") and "MATH 222" or "grad" or "maybe"',
 'COMP SCI 577': '("MATH 240" or "COMP SCI 240" or "STAT 475" or "COMP SCI 475" or "MATH 475") and ("COMP SCI 367" or "COMP SCI 400") or "grad" or "maybe"',
 'COMP SCI 578': '"COMP SCI 300" or "COMP SCI 367" or "grad" or "maybe"',
 'COMP SCI 579': '"maybe"',
 'DS 579': '"maybe"',
 'COMP SCI 611': '"maybe"',
 'L I S 611': '"maybe"',
 'COMP SCI 612': '"maybe"',
 'L I S 612': '"maybe"',
 'COMP SCI 613': '"maybe"',
 'L I S 613': '"maybe"',
 'COMP SCI 614': '"maybe"',
 'L I S 614': '"maybe"',
 'COMP SCI 635': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" and ("COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "L I S 102" or "COMP SCI 102") or "grad" or "maybe"',
 'I SY E 635': '"MATH 320" or "MATH 340" or "MATH 341" or "MATH 375" and ("COMP SCI 200" or "COMP SCI 220" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "L I S 102" or "COMP SCI 102") or "grad" or "maybe"',
 'COMP SCI 638': '"COMP SCI 200" or "COMP SCI 300" or "COMP SCI 301" or "COMP SCI 302" or "COMP SCI 310" or "COMP SCI 367" or "L I S 102" or "COMP SCI 102" or "grad" or "maybe"',
 'COMP SCI 639': 'None',
 'COMP SCI 640': '"COMP SCI 537" or "grad" or "maybe"',
 'COMP SCI 642': '"COMP SCI 537" or "grad" or "maybe"',
 'COMP SCI 681': '"maybe"',
 'COMP SCI 682': '"maybe"',
 'COMP SCI 691': '"maybe"',
 'COMP SCI 692': '"maybe"',
 'COMP SCI 698': '"maybe"',
 'COMP SCI 699': '"maybe"',
 'COMP SCI 701': '"grad"',
 'COMP SCI 702': '"maybe"',
 'COMP SCI 703': '"grad"',
 'COMP SCI 704': '"grad"',
 'COMP SCI 706': '"grad"',
 'COMP SCI 707': '"grad"',
 'E C E 707': '"grad"',
 'COMP SCI 710': '"grad"',
 'COMP SCI 714': '"grad" or "maybe"',
 'MATH 714': '"grad" or "maybe"',
 'COMP SCI 715': '"grad" or "maybe"',
 'MATH 715': '"grad" or "maybe"',
 'COMP SCI 719': '"grad"',
 'I SY E 719': '"grad"',
 'COMP SCI 722': '"grad"',
 'B M I 722': '"grad"',
 'E C E 722': '"grad"',
 'MED PHYS 722': '"grad"',
 'COMP SCI 723': '"grad"',
 'I SY E 723': '"grad"',
 'COMP SCI 726': '"grad"',
 'I SY E 726': '"grad"',
 'MATH 726': '"grad"',
 'STAT 726': '"grad"',
 'COMP SCI 727': '"grad"',
 'I SY E 727': '"grad"',
 'COMP SCI 728': '"grad"',
 'I SY E 728': '"grad"',
 'MATH 728': '"grad"',
 'COMP SCI 730': '"STAT 726" or "COMP SCI 726" or "I SY E 726" or "MATH 726"',
 'I SY E 730': '"STAT 726" or "COMP SCI 726" or "I SY E 726" or "MATH 726"',
 'MATH 730': '"STAT 726" or "COMP SCI 726" or "I SY E 726" or "MATH 726"',
 'COMP SCI 736': '"grad"',
 'COMP SCI 739': '"COMP SCI 736"',
 'COMP SCI 740': '"grad"',
 'COMP SCI 744': '"grad"',
 'COMP SCI 750': '"grad"',
 'E C E 750': '"grad"',
 'COMP SCI 752': '"grad"',
 'E C E 752': '"grad"',
 'COMP SCI 755': '"grad"',
 'E C E 755': '"grad"',
 'COMP SCI 756': '"grad"',
 'E C E 756': '"grad"',
 'COMP SCI 757': '"grad"',
 'E C E 757': '"grad"',
 'COMP SCI 758': '"grad"',
 'COMP SCI 759': '"grad"',
 'E C E 759': '"grad"',
 'E M A 759': '"grad"',
 'E P 759': '"grad"',
 'M E 759': '"grad"',
 'COMP SCI 760': '"grad"',
 'E C E 760': '"grad"',
 'COMP SCI 761': '"grad"',
 'E C E 761': '"grad"',
 'COMP SCI 762': '"E C E 760" or "COMP SCI 760"',
 'COMP SCI 763': '"grad"',
 'COMP SCI 764': '"grad"',
 'COMP SCI 765': '"grad"',
 'COMP SCI 766': '"grad"',
 'E C E 766': '"grad"',
 'COMP SCI 767': '"grad"',
 'B M I 767': '"grad"',
 'COMP SCI 769': '"grad"',
 'COMP SCI 770': '"grad"',
 'ED PSYCH 770': '"grad"',
 'PSYCH 770': '"grad"',
 'COMP SCI 771': '"grad"',
 'B M I 771': '"grad"',
 'COMP SCI 775': '"grad"',
 'B M I 775': '"grad"',
 'COMP SCI 776': '"grad"',
 'B M I 776': '"grad"',
 'COMP SCI 782': '"grad"',
 'E C E 782': '"grad"',
 'COMP SCI 784': '"grad"',
 'COMP SCI 787': '"grad"',
 'COMP SCI 790': '"maybe"',
 'COMP SCI 799': '"grad"',
 'COMP SCI 809': '"grad"',
 'COMP SCI 812': '"grad"',
 'COMP SCI 838': '"grad"',
 'COMP SCI 839': '"grad"',
 'COMP SCI 841': '"grad"',
 'B M I 841': '"grad"',
 'PSYCH 841': '"grad"',
 'COMP SCI 861': '"E C E 761" or "COMP SCI 761" or "E C E 830"',
 'E C E 861': '"E C E 761" or "COMP SCI 761" or "E C E 830"',
 'STAT 861': '"E C E 761" or "COMP SCI 761" or "E C E 830"',
 'COMP SCI 880': '"grad"',
 'COMP SCI 899': '"maybe"',
 'COMP SCI 900': '"maybe"',
 'COMP SCI 915': '"maybe"',
 'B M E 915': '"maybe"',
 'B M I 915': '"maybe"',
 'BIOCHEM 915': '"maybe"',
 'CBE 915': '"maybe"',
 'GENETICS 915': '"maybe"',
 'COMP SCI 990': '"maybe"',
 'COMP SCI 999': '"maybe"'}
uri = "mongodb+srv://rcbenson:fQGUWuiDCaKaGNQR@cluster0.zc0ssjv.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
try:
    client.admin.command('ping')
except Exception as e:
    print("connection failed")
db = client['EnrollmentHelper']
def build_expression(s):
    count = 0
    result = ""
    for char in s:
        if char == '"':
            count += 1
            if count % 2 == 0:
                result += '" in s'
            else:
                result += char
        else:
            result += char
    return result

def get_valid(c, s):
    """
    C is the course the student wishes to take.
    S is the set of requirements the student has fulfilled
    Returns 2 for can take, 1 for maybe, 0 for can't take
    """
    exp = build_expression(courseReqs[c])
    if eval(exp):
        return 2
    elif "maybe" in exp:
        return 1
    return 0

def fillsReq(c, reqs, toTake):
    """
    c is the course the student wishes to take.
    reqs is the set of requirements the student has fulfilled
    toTake is the set of classes that can fill a major req
    Returns 1 for is an unfilled major req, 0 for isn't
    """
    if c in reqs:
        return 0
    if c in toTake:
        return 1
    return 0

def signup(username, password, email, isGrad):
    """
    Returns string indicating success or failure type
    """
    if db['User'].find_one({"username" : username}):
        return "User already exists"
    if '@' not in email:
        return "Invalid email"
    db['User'].insert_one({'username': username, 'email': email, 'password': password, 'friends': [], "isGrad" : isGrad == "true"})
    return "Success"
def login(username, password):
    if db['User'].find_one({"username" : username, "password" : password}):
        return "Success"
    else:
        return "Failed login"
    
def addFriend(selfname, friendname):
    """
    Returns string indicating success or failure type
    """
    user = db['User'].find_one({"username" : selfname})
    if not user:
        return "User does not exist (should not happen as user is provided by frontend, not user)"
    if friendname not in user["friends"]:
        newval = {"$push": {"friends": friendname}}
        db['User'].update_one({"username" : selfname}, newval)
    return f"Added {friendname} to friends"

def findFriendClasses(selfname):
    """
    Returns dictionary of tuples matching a specific class, lecture, and lab to a list of friends
    as such: {(class, lec, lab) : [friends]}
    """
    friendClasses = {} #{(class, lec, lab) : [friends]}
    user = db['User'].find_one({"username" : selfname})
    if not user:
        return []
    for friend in user["friends"]:
        f = db['User'].find_one({"username" : friend})
        if not f or selfname not in f["friends"]:
            continue
        sched = db["Schedule"].find_one({"username": f["username"]})
        if not sched:
            continue
        for i in range(len(sched["taking"])):
            classLecLab = (sched["taking"][i], sched["lecture"][i], sched["lab"][i])
            if friend in friendClasses:
                friendClasses[friend].append(classLecLab)
            else:
                friendClasses[friend] = [classLecLab]
    return friendClasses

def getFriends(selfname):
    """
    Returns list of friends, or an empty list if something goes wrong
    """
    user = db['User'].find_one({"username" : selfname})
    if not user:
        return []
    return user["friends"]

def getHighlights(selfname):
    """
    Returns a dictionary of highlights in the form of {course: (canTake, fillsReq)}

    Where canTake = 0 if can't take, 1 if maybe can take (special cases), 2 if can take 
    and fillsReq = 0 if it doesn't fill a requirement, 1 if it does
    """
    user = db["DARS"].find_one({"username" : selfname})
    if not user:
        return {}
    reqs = set(user["c-taken"])
    toTake = set(user["c-required"])
    highlights = {}
    for c in courseReqs:
        highlights[c] = (get_valid(c, reqs), fillsReq(c, reqs, toTake))
    return highlights

def createDARS(username, taken, required):
    """
    Creates 
    """
    user = db['User'].find_one({"username" : username})
    if user and user["isGrad"]:
        taken.append("grad")
    if db['DARS'].find_one({"username" : username}):
        newval = {"$push": {'c-taken': taken, 'c-required': required}}
        db['DARS'].update_one({"username" : username}, newval)
    else:
        db['DARS'].insert_one({'username': username, 'c-taken': taken, 'c-required': required})
    return "Success"

