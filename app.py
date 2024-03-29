import hashlib
import os
from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from PIL import Image
import os
import mysql.connector
from mysql.connector import *
import random, string
import pdfkit
import calendar
from datetime import date
# from flask_wkhtmltopdf import Wkhtmltopdf

UPLOAD_FOLDER = 'static/images/'
# WKHTMLTOPDF_PATH = "C:/Program Files/wkhtmltopdf/bin"
# WKHTMLTOPDF_PATH = f'C:\Program Files\wkhtmltopdf\bin'
WKHTMLTOPDF_PATH = f'./wkhtmltopdf.exe'


app = Flask(__name__)
app.secret_key = "asndjaheh912yeuwbqduiqasgdyq"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# wkhtmltopdf = Wkhtmltopdf(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET" , "POST"])
def home():
    print("In Home Function")
    return render_template("login.html")
	# return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    print("In Login Function Without Post")
    global connection
    if request.method == "POST" and request.form["action"] == "login":
        print("In Login Function With Post and Action As Login")
        mail = request.form["email"]
        psw = request.form["password"]

        print(mail)
        print(psw)
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            query1 = "SELECT username FROM cred"
            cursor.execute(query1)
            user = cursor.fetchall()
            user = user[0][0]

            query2 = "SELECT password FROM cred"
            cursor.execute(query2)
            password = cursor.fetchall()
            password = password[0][0]

            plaintext = psw.encode()
            d = hashlib.md5(plaintext)
            hash = d.hexdigest()

            if mail == user:
                print("User Name Is Correct")
                if hash == password:
                    print("Password is Correct Now Go To Module Function")
                    return redirect(url_for('module'))
                else:
                    print("Wrong Password - Back To Login Page")
                    msg = "Wrong Password"
                    return render_template("login.html", msg = msg)
            else:
                print("User Name Is Wrong - Back To Login page")
                msg = "Wrong Username And Password"
                return render_template("login.html", msg = msg)

        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    if request.method == "POST" and request.form["action"] == "module":
        print("In Login Function With Post and Action As Module")
        value = request.form["password"]
        user = request.form["module"]

        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)
            data = [user]
            query = "SELECT password FROM cred WHERE type = %s"
            cursor.execute(query,data)
            password_data = cursor.fetchall()
            password_data = password_data[0][0]

            plaintext = value.encode()
            d = hashlib.md5(plaintext)
            hash = d.hexdigest()
            print(hash)

            if hash == password_data:
                print("Password Is Correct and Now Check For Username")
                if user == "payroll":
                    print("Username is correct now go to Dashboard Of Payroll")
                    return redirect(url_for('dashboard'))
                else:
                    print("Username Is Wrong So Back To The Password Page")
                    msg = "Wrong Credentials"
                    return render_template("password.html", msg=msg, value = user)

            else:
                print("Password Is Wrong So Back To Password Page")
                msg = "Wrong Password"
                return render_template("password.html", msg=msg , value = user)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return render_template('login.html')
#     return render_template('login.html')

@app.route("/expense", methods = ["POST" , "GET"])
def expense():
    # if request.method == "POST" and request.form["action"] == "esheet" :
    #     print("In Expense Sheet")
    #     return render_template("expense.html")
    if request.method == "POST" and request.form["action"] == "summary":
        print("In Summary")
        return render_template("expense2.html")

    elif request.method == "POST" and request.form["action"] == "find":
        return render_template("expense4.html")

    elif request.method == "POST" and request.form["action"] == "findData":
        month = request.form["mon"]
        year = request.form["year"]

        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            query1 = "SELECT Electricity,InternetBills,OfficeCleaner,ZoomRegistration,PublicationSubscription,Antivirus,Toners,MSWord,Domain,SundryOthers,PlantMaintenance,PostCourier,OfficeSupply,BusinessCard,TrainingEmployees,AnnualParty,ACMaintenance,PolycomCable,SundryOther1Desc,SundryOther1Amount,SundryOther2Desc,SundryOther2Amount,SundryOther3Desc,SundryOther3Amount,SundryOther4Desc,SundryOther4Amount,SundryOther5Desc,SundryOther5Amount,IndustryReport,DirectorAccomodation,EventExpense1Desc,EventExpense1Amount,EventExpense2Desc,EventExpense2Amount,EventExpense3Desc,EventExpense3Amount,EventExpense4Desc,EventExpense4Amount,ClientLunch,HotelCost,MIODMembership,RatingFees,LegalOther1Desc,LegalOther1Amount,LegalOther2Desc,LegalOther2Amount,LegalOther3Desc,LegalOther3Amount,LegalOther4Desc,LegalOther4Amount,LegalOther5Desc,LegalOther5Amount,Salary,Utilities,SundryExpenses,MarketingPromotioon,Regulatory,AuditFees,SecretarialFees,TravellingExpenses,BusinessMauritius,BusinessAfrica,CommunicationExpense,InsurancePremium,Depreciation,LegalProfessional,BankCharges,StaffWellfare,HeadOfficeExpense,RoyaltyPayable,Amortisation,FinanceCost,PaymentCart,OtherExpenses,OtherExpense1Desc,OtherExpense1Amount,OtherExpense2Desc,OtherExpense2Amount,OtherExpense3Desc,OtherExpense3Amount,OtherExpense4Desc,OtherExpense4Amount,OtherExpense5Desc,OtherExpense5Amount,Month,Year, IndependentDirectorFee FROM ExpenseInput WHERE Month = %s AND Year =%s"
            data = [month, year]
            cursor.execute(query1, data)

            get_data = cursor.fetchall()
            print(get_data)
            print(len(get_data))

            length = len(get_data)

            return render_template("expense3.html", length = length, data = get_data)

        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

        return render_template("expense4.html")

    elif request.method == "POST" and request.form["action"] == "period_data":
        from_month = request.form["from"]
        to_month = request.form["to"]

        from_year = request.form["fyear"]
        to_year = request.form["tyear"]

        # From Id
        fid = 0
        # To Id
        tid = 0

        if from_month == "January" or from_month=="january":
            print("In Jan")
            
            fid = "01"
        elif from_month == "February" or from_month=="february":
            print("In Feb")
            
            fid = "02"
        elif from_month == "March" or from_month=="march":
            print("In Mar")
            
            fid = "03"
        elif from_month == "April" or from_month=="april":
            print("In Apr")
            
            fid = "04"
        elif from_month == "May" or from_month=="may":
            print("In May")
            
            fid = "05"
        elif from_month == "June" or from_month=="june":
            print("In Jun")
            
            fid = "06"
        elif from_month == "July" or from_month=="july":
            print("In Jul")
            
            fid = "07"
        elif from_month == "August" or from_month=="august":
            print("In Aug")
            
            fid = "08"
        elif from_month == "September" or from_month=="september":
            print("In Sep")
            
            fid = "09"
        elif from_month == "October" or from_month=="october":
            print("In Oct")
            
            fid = "10"
        elif from_month == "November" or from_month=="november":
            print("In Nov")
            
            fid = "11"
        elif from_month == "December" or from_month=="december":
            print("In Dec")
            
            fid = "12"
        else:  
            print("In Else")
            msg = "Enter 'From' Month Correctly"
            return render_template("expense2.html", msg = msg)

# ==================================================================================================================================================

        if to_month == "January" or to_month=="january":
            print("In Jan")
            
            tid = "01"
        elif to_month == "February" or to_month=="february":
            print("In Feb")
            
            tid = "02"
        elif to_month == "March" or to_month=="march":
            print("In Mar")
            
            tid = "03"
        elif to_month == "April" or to_month=="april":
            print("In Apr")
            
            tid = "04"
        elif to_month == "May" or to_month=="may":
            print("In May")
            
            tid = "05"
        elif to_month == "June" or to_month=="june":
            print("In Jun")
            
            tid = "06"
        elif to_month == "July" or to_month=="july":
            print("In Jul")
            
            tid = "07"
        elif to_month == "August" or to_month=="august":
            print("In Aug")
            
            tid = "08"
        elif to_month == "September" or to_month=="september":
            print("In Sep")
            
            tid = "09"
        elif to_month == "October" or to_month=="october":
            print("In Oct")
            
            tid = "10"
        elif to_month == "November" or to_month=="november":
            print("In Nov")
            
            tid = "11"
        elif to_month == "December" or to_month=="december":
            print("In Dec")
            
            tid = "12"
        else:  
            print("In Else")
            msg = "Enter 'To' Month Correctly"
            return render_template("expense2.html", msg = msg)

        # from_date = "01-"+fid+"-"+from_year
        # to_date = "01-"+tid+"-"+to_year

        from_date = from_year+"-"+fid+"-01"
        to_date = to_year+"-"+tid+"-01"

        print("From Date ", from_date)
        print("To Date ", to_date)

        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            get_query = "SELECT salary, utilities,sundry,marketing,regulatory,audit,secretarial,travel,businessMAU,businessKEN,communication,insurance,depreciation,legal,bank,wellfare,headOffice,royalty,amortisation,finance,cart,other, OtherExpense1, OtherExpense2, OtherExpense3, OtherExpense4, OtherExpense5 ,total FROM expenses WHERE monthDate BETWEEN %s AND %s"
            data2 = [from_date , to_date]
                        
            cursor.execute(get_query, data2)
            get_data = cursor.fetchall()


            month_query = "SELECT month FROM expenses WHERE monthDate BETWEEN %s AND %s "
            # data = [fid, tid]
            cursor.execute(month_query, data2)
            month_data = cursor.fetchall()

            # print(month_data)

            length2 = len(month_data)
            length3 = length2 + 1
            
            length = len(get_data)

            # return render_template("expensesheet.html", data = get_data, length = length)
            return render_template("expensesheet2.html", data=get_data, length = length, data2 = month_data, length3 = length3)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    elif request.method == "POST" and request.form["action"] == "input":
        print("In Input")
        return render_template("expense.html")
    elif request.method == "POST" and request.form["action"] == "save":

        month = request.form["mon"]        
        
        id = ""
        if month == "January" or month=="january":
            print("In Jan")
            
            id = "01"
        elif month == "February" or month=="february":
            print("In Feb")
            
            id = "02"
        elif month == "March" or month=="march":
            print("In Mar")
            
            id = "03"
        elif month == "April" or month=="april":
            print("In Apr")
            
            id = "04"
        elif month == "May" or month=="may":
            print("In May")
            
            id = "05"
        elif month == "June" or month=="june":
            print("In Jun")
            
            id = "06"
        elif month == "July" or month=="july":
            print("In Jul")
            
            id = "07"
        elif month == "August" or month=="august":
            print("In Aug")
            
            id = "08"
        elif month == "September" or month=="september":
            print("In Sep")
            
            id = "09"
        elif month == "October" or month=="october":
            print("In Oct")
            
            id = "10"
        elif month == "November" or month=="november":
            print("In Nov")
            
            id = "11"
        elif month == "December" or month=="december":
            print("In Dec")
            
            id = "12"
        else:  
            print("In Else")
            msg = "Enter Month Correctly"
            return render_template("expense.html", msg = msg )

        year = request.form["year"]

        # mdate = "01-"+id+"-"+year
        mdate = year+"-"+id+"-01"
        
        print("date " , mdate)

        salary = request.form["sal"]
        if salary == "":
            print("In If")
            salary = 0
        print("salary ", salary)

        # rent = request.form["rent"]
        # if rent == "":
        #     print("In If")
        #     rent = 0
        # print("rent ", rent)
        rent = 0

        utilities = request.form["utl"]
        if utilities == "":
            print("In If")
            utilities = 0
        print("utilities ", utilities)
        
        sundry = request.form["sun"]
        if sundry == "":
            print("In If")
            sundry = 0
        print("sundry ", sundry)

        marketing = request.form["market"]
        if marketing == "":
            print("In If")
            marketing = 0
        print("marketing ", marketing)

        regulatory = request.form["reg"]
        if regulatory == "":
            print("In If")
            regulatory = 0
        print("regulatory ", regulatory)

        audit = request.form["aud"]
        if audit == "":
            print("In If")
            audit = 0
        print("audit ", audit)

        secretarial = request.form["secret"]
        if secretarial == "":
            print("In If")
            secretarial = 0
        print("secretarial ", secretarial)

        travel = request.form["travelexp"]
        if travel == "":
            print("In If")
            travel = 0
        print("travel ", travel)

        businessMAU = request.form["mbusiness"]
        if businessMAU == "":
            print("In If")
            businessMAU = 0
        print("businessMAU ", businessMAU)

        # Business Africa
        businessKEN = request.form["kbusiness"]
        if businessKEN == "":
            print("In If")
            businessKEN = 0
        print("businessKEN ", businessKEN)

        communication = request.form["comm"]
        if communication == "":
            print("In If")
            communication = 0
        print("communication ", communication)

        insurance = request.form["insure"]
        if insurance == "":
            print("In If")
            insurance = 0
        print("insurance ", insurance)

        depreciation = request.form["depr"]
        if depreciation == "":
            print("In If")
            depreciation = 0
        print("depreciation ", depreciation)

        legal = request.form["lprof"]
        if legal == "":
            print("In If")
            legal = 0
        print("legal ", legal)

        bank = request.form["bank"]
        if bank == "":
            print("In If")
            bank = 0
        print("bank ", bank)

        wellfare = request.form["staff"]
        if wellfare == "":
            print("In If")
            wellfare = 0
        print("wellfare " , wellfare)

        head = request.form["head"]
        if head == "":
            print("In If")
            head = 0
        print("head ", head)

        royalty = request.form["royal"]
        if royalty == "":
            print("In If")
            royalty = 0
        print("royalty ", royalty)

        amortisation = request.form["amor"]
        if amortisation == "":
            print("In If")
            amortisation = 0
        print("amortisation ", amortisation)

        finance = request.form["finance"]
        if finance == "":
            print("In If")
            finance = 0
        print("finance ", finance)
        
        cart = request.form["cart"]
        if cart == "":
            print("In If")
            cart = 0
        print(cart)

        other = request.form["otherexp"]
        if other == "":
            print("In If")
            other = 0
        print("other ", other)

        # Other Expense Of Main

        OtherExpense1Desc = request.form["othertotal1"]
        if OtherExpense1Desc == "":
            OtherExpense1Desc = " "

        OtherExpense2Desc = request.form["othertotal2"]
        if OtherExpense2Desc == "":
            OtherExpense2Desc = " "

        OtherExpense3Desc = request.form["othertotal3"]
        if OtherExpense3Desc == "":
            OtherExpense3Desc = " "

        OtherExpense4Desc = request.form["othertotal4"]
        if OtherExpense4Desc == "":
            OtherExpense4Desc = " "

        OtherExpense5Desc = request.form["othertotal5"]
        if OtherExpense5Desc == "":
            OtherExpense5Desc = " "


        OtherExpense1Amount = request.form["otherTotalExp1"]
        if OtherExpense1Amount == "":
            OtherExpense1Amount = 0

        OtherExpense2Amount = request.form["otherTotalExp2"]
        if OtherExpense2Amount == "":
            OtherExpense2Amount = 0

        OtherExpense3Amount = request.form["otherTotalExp3"]
        if OtherExpense3Amount == "":
            OtherExpense3Amount = 0

        OtherExpense4Amount = request.form["otherTotalExp4"]
        if OtherExpense4Amount == "":
            OtherExpense4Amount = 0

        OtherExpense5Amount = request.form["otherTotalExp5"]
        if OtherExpense5Amount == "":
            OtherExpense5Amount = 0

        total = int(salary) + int(utilities) + int(sundry) + int(marketing) + int(regulatory) + int(audit) + int(secretarial) + int(travel) + int(businessMAU) + int(businessKEN) + int(communication) + int(insurance) + int(depreciation) + int(legal) + int(bank) + int(wellfare) + int(head) + int(royalty) + int(amortisation) + int(finance) + int(cart) + int(other) + int(OtherExpense1Amount) + int(OtherExpense2Amount) + int(OtherExpense3Amount) + int(OtherExpense4Amount) + int(OtherExpense5Amount)
        # print("total ", total)

        if total == None:
            total = 0

# ====================================================================================================================================================================================================

        # Utilities Section
        Electricity = request.form["electric"]
        if Electricity == "":
            Electricity = 0

        InternetBills = request.form["inter"]
        if InternetBills == "":
            InternetBills = 0
        

        # Sundry Expenses
        OfficeCleaner = request.form["ofc"]
        if OfficeCleaner == "":
            OfficeCleaner = 0
        
        ZoomCharge = request.form["zoom"]
        if ZoomCharge == "":
            ZoomCharge = 0
        
        Publication = request.form["public"]
        if Publication == "":
            Publication = 0
        
        Antivirus = request.form["anti"]
        if Antivirus == "":
            Antivirus = 0
        
        toner = request.form["toner"]
        if toner == "":
            toner = 0
        
        MSWord = request.form["msofc"]
        if MSWord == "":
            MSWord = 0
        
        Domain = request.form["domain"]
        if Domain == "":
            Domain = 0
        
        SundryOthers = request.form["otherSun"]
        if SundryOthers == "":
            SundryOthers = 0
        
        PlantMaintenance = request.form["plant"]
        if PlantMaintenance == "":
            PlantMaintenance = 0
        
        PostCourier = request.form["cour"]
        if PostCourier == "":
            PostCourier = 0
        
        OfficeSupply = request.form["supply"]
        if OfficeSupply == "":
            OfficeSupply = 0
        
        Businesscard = request.form["bcard"]
        if Businesscard == "":
            Businesscard = 0
        
        TrainingEmployee = request.form["train"]
        if TrainingEmployee == "":
            TrainingEmployee = 0
        
        AnnualParty = request.form["annual"]
        if AnnualParty == "":
            AnnualParty = 0
        
        ACMaintenance = request.form["acmain"]
        if ACMaintenance == "":
            ACMaintenance = 0
        
        # PolycomCable = request.form["polycom"]
        # if PolycomCable == "":
        #     PolycomCable = 0

        PolycomCable = 0
        
        SundryOther1Desc = request.form["othersundry1"]
        if SundryOther1Desc == "":
            SundryOther1Desc = " "
        
        SundryOther1Amount = request.form["otherSundryExp1"]
        if SundryOther1Amount == "":
            SundryOther1Amount = 0
        
        SundryOther2Desc = request.form["othersundry2"]
        if SundryOther2Desc == "":
            SundryOther2Desc = " "
        
        SundryOther2Amount = request.form["otherSundryExp2"]
        if SundryOther2Amount == "":
            SundryOther2Amount = 0
        
        SundryOther3Desc = request.form["othersundry3"]
        if SundryOther3Desc == "":
            SundryOther3Desc = " "
        
        SundryOther3Amount = request.form["otherSundryExp3"]
        if SundryOther3Amount == "":
            SundryOther3Amount = 0
        
        SundryOther4Desc = request.form["othersundry4"]
        if SundryOther4Desc == "":
            SundryOther4Desc = " "
        
        SundryOther4Amount = request.form["otherSundryExp4"]
        if SundryOther4Amount == "":
            SundryOther4Amount = 0
        
        SundryOther5Desc = request.form["othersundry5"]
        if SundryOther5Desc == "":
            SundryOther5Desc = " "
        
        SundryOther5Amount = request.form["otherSundryExp5"]
        if SundryOther5Amount == "":
            SundryOther5Amount = 0
        

        # Business Promotion Expenses Mauritius

        IndustryReports = request.form["industry"]
        if IndustryReports == "":
            IndustryReports = 0
        
        DirectorAccomodation = request.form["stay"]
        if DirectorAccomodation == "":
            DirectorAccomodation = 0
        
        EventExpense1Desc = request.form["event1"]
        if EventExpense1Desc == "":
            EventExpense1Desc = " "
        
        EventExpense1Amount = request.form["eveExp1"]
        if EventExpense1Amount == "":
            EventExpense1Amount = 0
        
        EventExpense2Desc = request.form["event2"]
        if EventExpense2Desc == "":
            EventExpense2Desc = " "
        
        EventExpense2Amount = request.form["eveExp2"]
        if EventExpense2Amount == "":
            EventExpense2Amount = 0
        
        EventExpense3Desc = request.form["event3"]
        if EventExpense3Desc == "":
            EventExpense3Desc = " "
        
        EventExpense3Amount = request.form["eveExp3"]
        if EventExpense3Amount == "":
            EventExpense3Amount = 0
        
        EventExpense4Desc = request.form["event4"]
        if EventExpense4Desc == "":
            EventExpense4Desc = " "
        
        EventExpense4Amount = request.form["eveExp4"]
        if EventExpense4Amount == "":
            EventExpense4Amount = 0
        
        ClientLunch = request.form["lunch"]
        if ClientLunch == "":
            ClientLunch = 0
        
        # HotelCost = request.form["inter"]
        # if HotelCost == "":
        #     HotelCost = 0
        
        HotelCost = 0

        MIODMembership = request.form["member"]
        if MIODMembership == "":
            MIODMembership = 0
        

        # Legal & Professional Expenses

        RatingFees = request.form["rating"]
        if RatingFees == "":
            RatingFees = 0

        DirectorFees = request.form["independent"]
        if DirectorFees == "":
            DirectorFees = 0
        
        LegalOther1Desc = request.form["other1"]
        if LegalOther1Desc == "":
            LegalOther1Desc = " "
        
        LegalOther1Amount = request.form["otherExp1"]
        if LegalOther1Amount == "":
            LegalOther1Amount = 0
        
        LegalOther2Desc = request.form["other2"]
        if LegalOther2Desc == "":
            LegalOther2Desc = " "
        
        LegalOther2Amount = request.form["otherExp2"]
        if LegalOther2Amount == "":
            LegalOther2Amount = 0
        
        LegalOther3Desc = request.form["other3"]
        if LegalOther3Desc == "":
            LegalOther3Desc = " "
        
        LegalOther3Amount = request.form["otherExp3"]
        if LegalOther3Amount == "":
            LegalOther3Amount = 0
        
        LegalOther4Desc = request.form["other4"]
        if LegalOther4Desc == "":
            LegalOther4Desc = " "
        
        LegalOther4Amount = request.form["otherExp4"]
        if LegalOther4Amount == "":
            LegalOther4Amount = 0
        
        LegalOther5Desc = request.form["other5"]
        if LegalOther5Desc == "":
            LegalOther5Desc = " "
        
        LegalOther5Amount = request.form["otherExp5"]
        if LegalOther5Amount == "":
            LegalOther5Amount = 0


        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            get_process = "SELECT process FROM expenses WHERE month = %s"
            data_month = [month]
            cursor.execute(get_process, data_month)
            process = cursor.fetchall()

            # print(process)

            if process == []:
                proc = "No" 
            else:
                proc = "Yes"

            if proc == "No":

                insert_query = """INSERT INTO expenses(
                                salary,
                                rent,
                                utilities,
                                sundry,
                                marketing,
                                regulatory,
                                audit,
                                secretarial,
                                travel,
                                businessMAU,
                                businessKEN,
                                communication,
                                insurance,
                                depreciation,
                                legal,
                                bank,
                                wellfare,
                                headOffice,
                                royalty,
                                amortisation,
                                finance,
                                cart,
                                other,
                                OtherExpense1,
                                OtherExpense2,
                                OtherExpense3,
                                OtherExpense4,
                                OtherExpense5,
                                total,
                                process,
                                month,
                                year,
                                monthDigit,
                                monthDate)
                                VALUES
                                (
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                                );
                                """
                data = [salary, rent, utilities, sundry, marketing, regulatory, audit, secretarial, travel, businessMAU, businessKEN, communication, insurance, depreciation, legal, bank, wellfare, head, royalty, amortisation, finance, cart, other, OtherExpense1Amount, OtherExpense2Amount, OtherExpense3Amount, OtherExpense4Amount, OtherExpense5Amount , total, "Yes", month, year, id, mdate]
                cursor.execute(insert_query, data)

                print("Insert Query Executed")

                insert_all = """INSERT INTO ExpenseInput(
                                Electricity,
                                InternetBills,
                                OfficeCleaner,
                                ZoomRegistration,
                                PublicationSubscription,
                                Antivirus,
                                Toners,
                                MSWord,
                                Domain,
                                SundryOthers,
                                PlantMaintenance,
                                PostCourier,
                                OfficeSupply,
                                BusinessCard,
                                TrainingEmployees,
                                AnnualParty,
                                ACMaintenance,
                                PolycomCable,
                                SundryOther1Desc,
                                SundryOther1Amount,
                                SundryOther2Desc,
                                SundryOther2Amount,
                                SundryOther3Desc,
                                SundryOther3Amount,
                                SundryOther4Desc,
                                SundryOther4Amount,
                                SundryOther5Desc,
                                SundryOther5Amount,
                                IndustryReport,
                                DirectorAccomodation,
                                EventExpense1Desc,
                                EventExpense1Amount,
                                EventExpense2Desc,
                                EventExpense2Amount,
                                EventExpense3Desc,
                                EventExpense3Amount,
                                EventExpense4Desc,
                                EventExpense4Amount,
                                ClientLunch,
                                HotelCost,
                                MIODMembership,
                                RatingFees,
                                IndependentDirectorFee,
                                LegalOther1Desc,
                                LegalOther1Amount,
                                LegalOther2Desc,
                                LegalOther2Amount,
                                LegalOther3Desc,
                                LegalOther3Amount,
                                LegalOther4Desc,
                                LegalOther4Amount,
                                LegalOther5Desc,
                                LegalOther5Amount,
                                Salary,
                                Utilities,
                                SundryExpenses,
                                MarketingPromotioon,
                                Regulatory,
                                AuditFees,
                                SecretarialFees,
                                TravellingExpenses,
                                BusinessMauritius,
                                BusinessAfrica,
                                CommunicationExpense,
                                InsurancePremium,
                                Depreciation,
                                LegalProfessional,
                                BankCharges,
                                StaffWellfare,
                                HeadOfficeExpense,
                                RoyaltyPayable,
                                Amortisation,
                                FinanceCost,
                                PaymentCart,
                                OtherExpenses,
                                OtherExpense1Desc,
                                OtherExpense1Amount,
                                OtherExpense2Desc,
                                OtherExpense2Amount,
                                OtherExpense3Desc,
                                OtherExpense3Amount,
                                OtherExpense4Desc,
                                OtherExpense4Amount,
                                OtherExpense5Desc,
                                OtherExpense5Amount,
                                Month,
                                Year)
                                VALUES(
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s);
                                """
                all_data = [Electricity, InternetBills, OfficeCleaner, ZoomCharge, Publication, Antivirus, toner, MSWord, Domain, SundryOthers, PlantMaintenance, PostCourier, OfficeSupply, Businesscard, TrainingEmployee, AnnualParty, ACMaintenance, PolycomCable, SundryOther1Desc, SundryOther1Amount, SundryOther2Desc, SundryOther2Amount, SundryOther3Desc, SundryOther3Amount, SundryOther4Desc, SundryOther4Amount, SundryOther5Desc, SundryOther5Amount, IndustryReports, DirectorAccomodation, EventExpense1Desc, EventExpense1Amount, EventExpense2Desc, EventExpense2Amount, EventExpense3Desc, EventExpense3Amount, EventExpense4Desc, EventExpense4Amount, ClientLunch, HotelCost, MIODMembership, RatingFees, DirectorFees , LegalOther1Desc, LegalOther1Amount, LegalOther2Desc, LegalOther2Amount, LegalOther3Desc, LegalOther3Amount, LegalOther4Desc, LegalOther4Amount, LegalOther5Desc, LegalOther5Amount, salary, utilities, sundry, marketing, regulatory, audit, secretarial, travel, businessMAU, businessKEN, communication, insurance, depreciation, legal, bank, wellfare, head, royalty, amortisation, finance, cart, other, OtherExpense1Desc, OtherExpense1Amount, OtherExpense2Desc, OtherExpense2Amount, OtherExpense3Desc, OtherExpense3Amount, OtherExpense4Desc, OtherExpense4Amount, OtherExpense5Desc, OtherExpense5Amount, month, year]
                cursor.execute(insert_all, all_data)

                print("All Data Query Executed")


                msg = "Expense Added Successfully"
            else:
                msg = "Expense Already Added"
            return render_template("expense.html", msg=msg)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        
    # elif request.method == "POST" and request.form["action"] == "update":
        
    #     return render_template("expense4.html")

    elif request.method == "POST" and request.form["action"] == "update":

        month = request.form["mon"]        
        
        id = ""
        if month == "January" or month=="january":
            print("In Jan")
            
            id = "01"
        elif month == "February" or month=="february":
            print("In Feb")
            
            id = "02"
        elif month == "March" or month=="march":
            print("In Mar")
            
            id = "03"
        elif month == "April" or month=="april":
            print("In Apr")
            
            id = "04"
        elif month == "May" or month=="may":
            print("In May")
            
            id = "05"
        elif month == "June" or month=="june":
            print("In Jun")
            
            id = "06"
        elif month == "July" or month=="july":
            print("In Jul")
            
            id = "07"
        elif month == "August" or month=="august":
            print("In Aug")
            
            id = "08"
        elif month == "September" or month=="september":
            print("In Sep")
            
            id = "09"
        elif month == "October" or month=="october":
            print("In Oct")
            
            id = "10"
        elif month == "November" or month=="november":
            print("In Nov")
            
            id = "11"
        elif month == "December" or month=="december":
            print("In Dec")
            
            id = "12"
        else:  
            print("In Else")
            msg = "Enter Month Correctly"
            return render_template("expense.html", msg = msg )

        year = request.form["year"]

        # mdate = "01-"+id+"-"+year
        mdate = year+"-"+id+"-01"
        
        print("date " , mdate)

        salary = request.form["sal"]
        if salary == "":
            print("In If")
            salary = 0
        print("salary ", salary)

        # rent = request.form["rent"]
        # if rent == "":
        #     print("In If")
        #     rent = 0
        # print("rent ", rent)
        rent = 0

        utilities = request.form["utl"]
        if utilities == "":
            print("In If")
            utilities = 0
        print("utilities ", utilities)
        
        sundry = request.form["sun"]
        if sundry == "":
            print("In If")
            sundry = 0
        print("sundry ", sundry)

        marketing = request.form["market"]
        if marketing == "":
            print("In If")
            marketing = 0
        print("marketing ", marketing)

        regulatory = request.form["reg"]
        if regulatory == "":
            print("In If")
            regulatory = 0
        print("regulatory ", regulatory)

        audit = request.form["aud"]
        if audit == "":
            print("In If")
            audit = 0
        print("audit ", audit)

        secretarial = request.form["secret"]
        if secretarial == "":
            print("In If")
            secretarial = 0
        print("secretarial ", secretarial)

        travel = request.form["travelexp"]
        if travel == "":
            print("In If")
            travel = 0
        print("travel ", travel)

        businessMAU = request.form["mbusiness"]
        if businessMAU == "":
            print("In If")
            businessMAU = 0
        print("businessMAU ", businessMAU)

        # Business Africa
        businessKEN = request.form["kbusiness"]
        if businessKEN == "":
            print("In If")
            businessKEN = 0
        print("businessKEN ", businessKEN)

        communication = request.form["comm"]
        if communication == "":
            print("In If")
            communication = 0
        print("communication ", communication)

        insurance = request.form["insure"]
        if insurance == "":
            print("In If")
            insurance = 0
        print("insurance ", insurance)

        depreciation = request.form["depr"]
        if depreciation == "":
            print("In If")
            depreciation = 0
        print("depreciation ", depreciation)

        legal = request.form["lprof"]
        if legal == "":
            print("In If")
            legal = 0
        print("legal ", legal)

        bank = request.form["bank"]
        if bank == "":
            print("In If")
            bank = 0
        print("bank ", bank)

        wellfare = request.form["staff"]
        if wellfare == "":
            print("In If")
            wellfare = 0
        print("wellfare " , wellfare)

        head = request.form["head"]
        if head == "":
            print("In If")
            head = 0
        print("head ", head)

        royalty = request.form["royal"]
        if royalty == "":
            print("In If")
            royalty = 0
        print("royalty ", royalty)

        amortisation = request.form["amor"]
        if amortisation == "":
            print("In If")
            amortisation = 0
        print("amortisation ", amortisation)

        finance = request.form["finance"]
        if finance == "":
            print("In If")
            finance = 0
        print("finance ", finance)
        
        cart = request.form["cart"]
        if cart == "":
            print("In If")
            cart = 0
        print(cart)

        other = request.form["otherexp"]
        if other == "":
            print("In If")
            other = 0
        print("other ", other)

        # Other Expense Of Main

        OtherExpense1Desc = request.form["othertotal1"]
        if OtherExpense1Desc == "":
            OtherExpense1Desc = " "

        OtherExpense2Desc = request.form["othertotal2"]
        if OtherExpense2Desc == "":
            OtherExpense2Desc = " "

        OtherExpense3Desc = request.form["othertotal3"]
        if OtherExpense3Desc == "":
            OtherExpense3Desc = " "

        OtherExpense4Desc = request.form["othertotal4"]
        if OtherExpense4Desc == "":
            OtherExpense4Desc = " "

        OtherExpense5Desc = request.form["othertotal5"]
        if OtherExpense5Desc == "":
            OtherExpense5Desc = " "


        OtherExpense1Amount = request.form["otherTotalExp1"]
        if OtherExpense1Amount == "":
            OtherExpense1Amount = 0

        OtherExpense2Amount = request.form["otherTotalExp2"]
        if OtherExpense2Amount == "":
            OtherExpense2Amount = 0

        OtherExpense3Amount = request.form["otherTotalExp3"]
        if OtherExpense3Amount == "":
            OtherExpense3Amount = 0

        OtherExpense4Amount = request.form["otherTotalExp4"]
        if OtherExpense4Amount == "":
            OtherExpense4Amount = 0

        OtherExpense5Amount = request.form["otherTotalExp5"]
        if OtherExpense5Amount == "":
            OtherExpense5Amount = 0

        total = int(salary) + int(utilities) + int(sundry) + int(marketing) + int(regulatory) + int(audit) + int(secretarial) + int(travel) + int(businessMAU) + int(businessKEN) + int(communication) + int(insurance) + int(depreciation) + int(legal) + int(bank) + int(wellfare) + int(head) + int(royalty) + int(amortisation) + int(finance) + int(cart) + int(other) + int(OtherExpense1Amount) + int(OtherExpense2Amount) + int(OtherExpense3Amount) + int(OtherExpense4Amount) + int(OtherExpense5Amount)
        # print("total ", total)

        if total == None:
            total = 0

# ====================================================================================================================================================================================================

        # Utilities Section
        Electricity = request.form["electric"]
        if Electricity == "":
            Electricity = 0

        InternetBills = request.form["inter"]
        if InternetBills == "":
            InternetBills = 0
        

        # Sundry Expenses
        OfficeCleaner = request.form["ofc"]
        if OfficeCleaner == "":
            OfficeCleaner = 0
        
        ZoomCharge = request.form["zoom"]
        if ZoomCharge == "":
            ZoomCharge = 0
        
        Publication = request.form["public"]
        if Publication == "":
            Publication = 0
        
        Antivirus = request.form["anti"]
        if Antivirus == "":
            Antivirus = 0
        
        toner = request.form["toner"]
        if toner == "":
            toner = 0
        
        MSWord = request.form["msofc"]
        if MSWord == "":
            MSWord = 0
        
        Domain = request.form["domain"]
        if Domain == "":
            Domain = 0
        
        SundryOthers = request.form["otherSun"]
        if SundryOthers == "":
            SundryOthers = 0
        
        PlantMaintenance = request.form["plant"]
        if PlantMaintenance == "":
            PlantMaintenance = 0
        
        PostCourier = request.form["cour"]
        if PostCourier == "":
            PostCourier = 0
        
        OfficeSupply = request.form["supply"]
        if OfficeSupply == "":
            OfficeSupply = 0
        
        Businesscard = request.form["bcard"]
        if Businesscard == "":
            Businesscard = 0
        
        TrainingEmployee = request.form["train"]
        if TrainingEmployee == "":
            TrainingEmployee = 0
        
        AnnualParty = request.form["annual"]
        if AnnualParty == "":
            AnnualParty = 0
        
        ACMaintenance = request.form["acmain"]
        if ACMaintenance == "":
            ACMaintenance = 0
        
        # PolycomCable = request.form["polycom"]
        # if PolycomCable == "":
        #     PolycomCable = 0

        PolycomCable = 0
        
        SundryOther1Desc = request.form["othersundry1"]
        if SundryOther1Desc == "":
            SundryOther1Desc = " "
        
        SundryOther1Amount = request.form["otherSundryExp1"]
        if SundryOther1Amount == "":
            SundryOther1Amount = 0
        
        SundryOther2Desc = request.form["othersundry2"]
        if SundryOther2Desc == "":
            SundryOther2Desc = " "
        
        SundryOther2Amount = request.form["otherSundryExp2"]
        if SundryOther2Amount == "":
            SundryOther2Amount = 0
        
        SundryOther3Desc = request.form["othersundry3"]
        if SundryOther3Desc == "":
            SundryOther3Desc = " "
        
        SundryOther3Amount = request.form["otherSundryExp3"]
        if SundryOther3Amount == "":
            SundryOther3Amount = 0
        
        SundryOther4Desc = request.form["othersundry4"]
        if SundryOther4Desc == "":
            SundryOther4Desc = " "
        
        SundryOther4Amount = request.form["otherSundryExp4"]
        if SundryOther4Amount == "":
            SundryOther4Amount = 0
        
        SundryOther5Desc = request.form["othersundry5"]
        if SundryOther5Desc == "":
            SundryOther5Desc = " "
        
        SundryOther5Amount = request.form["otherSundryExp5"]
        if SundryOther5Amount == "":
            SundryOther5Amount = 0
        

        # Business Promotion Expenses Mauritius

        IndustryReports = request.form["industry"]
        if IndustryReports == "":
            IndustryReports = 0
        
        DirectorAccomodation = request.form["stay"]
        if DirectorAccomodation == "":
            DirectorAccomodation = 0
        
        EventExpense1Desc = request.form["event1"]
        if EventExpense1Desc == "":
            EventExpense1Desc = " "
        
        EventExpense1Amount = request.form["eveExp1"]
        if EventExpense1Amount == "":
            EventExpense1Amount = 0
        
        EventExpense2Desc = request.form["event2"]
        if EventExpense2Desc == "":
            EventExpense2Desc = " "
        
        EventExpense2Amount = request.form["eveExp2"]
        if EventExpense2Amount == "":
            EventExpense2Amount = 0
        
        EventExpense3Desc = request.form["event3"]
        if EventExpense3Desc == "":
            EventExpense3Desc = " "
        
        EventExpense3Amount = request.form["eveExp3"]
        if EventExpense3Amount == "":
            EventExpense3Amount = 0
        
        EventExpense4Desc = request.form["event4"]
        if EventExpense4Desc == "":
            EventExpense4Desc = " "
        
        EventExpense4Amount = request.form["eveExp4"]
        if EventExpense4Amount == "":
            EventExpense4Amount = 0
        
        ClientLunch = request.form["lunch"]
        if ClientLunch == "":
            ClientLunch = 0
        
        # HotelCost = request.form["inter"]
        # if HotelCost == "":
        #     HotelCost = 0
        
        HotelCost = 0

        MIODMembership = request.form["member"]
        if MIODMembership == "":
            MIODMembership = 0
        

        # Legal & Professional Expenses

        RatingFees = request.form["rating"]
        if RatingFees == "":
            RatingFees = 0

        DirectorFees = request.form["independent"]
        if DirectorFees == "":
            DirectorFees = 0
        
        LegalOther1Desc = request.form["other1"]
        if LegalOther1Desc == "":
            LegalOther1Desc = " "
        
        LegalOther1Amount = request.form["otherExp1"]
        if LegalOther1Amount == "":
            LegalOther1Amount = 0
        
        LegalOther2Desc = request.form["other2"]
        if LegalOther2Desc == "":
            LegalOther2Desc = " "
        
        LegalOther2Amount = request.form["otherExp2"]
        if LegalOther2Amount == "":
            LegalOther2Amount = 0
        
        LegalOther3Desc = request.form["other3"]
        if LegalOther3Desc == "":
            LegalOther3Desc = " "
        
        LegalOther3Amount = request.form["otherExp3"]
        if LegalOther3Amount == "":
            LegalOther3Amount = 0
        
        LegalOther4Desc = request.form["other4"]
        if LegalOther4Desc == "":
            LegalOther4Desc = " "
        
        LegalOther4Amount = request.form["otherExp4"]
        if LegalOther4Amount == "":
            LegalOther4Amount = 0
        
        LegalOther5Desc = request.form["other5"]
        if LegalOther5Desc == "":
            LegalOther5Desc = " "
        
        LegalOther5Amount = request.form["otherExp5"]
        if LegalOther5Amount == "":
            LegalOther5Amount = 0

        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            update_all = """
                            UPDATE ExpenseInput
                            SET
                            Electricity = %s,
                            InternetBills = %s,
                            OfficeCleaner = %s,
                            ZoomRegistration = %s,
                            PublicationSubscription = %s,
                            Antivirus = %s,
                            Toners = %s,
                            MSWord = %s,
                            Domain = %s,
                            SundryOthers = %s,
                            PlantMaintenance = %s,
                            PostCourier = %s,
                            OfficeSupply = %s,
                            BusinessCard = %s,
                            TrainingEmployees = %s,
                            AnnualParty = %s,
                            ACMaintenance = %s,
                            PolycomCable = %s,
                            SundryOther1Desc = %s,
                            SundryOther1Amount = %s,
                            SundryOther2Desc = %s,
                            SundryOther2Amount = %s,
                            SundryOther3Desc = %s,
                            SundryOther3Amount = %s,
                            SundryOther4Desc = %s,
                            SundryOther4Amount = %s,
                            SundryOther5Desc = %s,
                            SundryOther5Amount = %s,
                            IndustryReport = %s,
                            DirectorAccomodation = %s,
                            EventExpense1Desc = %s,
                            EventExpense1Amount = %s,
                            EventExpense2Desc = %s,
                            EventExpense2Amount = %s,
                            EventExpense3Desc = %s,
                            EventExpense3Amount = %s,
                            EventExpense4Desc = %s,
                            EventExpense4Amount = %s,
                            ClientLunch = %s,
                            HotelCost = %s,
                            MIODMembership = %s,
                            RatingFees = %s,
                            IndependentDirectorFee = %s,
                            LegalOther1Desc = %s,
                            LegalOther1Amount = %s,
                            LegalOther2Desc = %s,
                            LegalOther2Amount = %s,
                            LegalOther3Desc = %s,
                            LegalOther3Amount = %s,
                            LegalOther4Desc = %s,
                            LegalOther4Amount = %s,
                            LegalOther5Desc = %s,
                            LegalOther5Amount = %s,
                            Salary = %s,
                            Utilities = %s,
                            SundryExpenses = %s,
                            MarketingPromotioon = %s,
                            Regulatory = %s,
                            AuditFees = %s,
                            SecretarialFees = %s,
                            TravellingExpenses = %s,
                            BusinessMauritius = %s,
                            BusinessAfrica = %s,
                            CommunicationExpense = %s,
                            InsurancePremium = %s,
                            Depreciation = %s,
                            LegalProfessional = %s,
                            BankCharges = %s,
                            StaffWellfare = %s,
                            HeadOfficeExpense = %s,
                            RoyaltyPayable = %s,
                            Amortisation = %s,
                            FinanceCost = %s,
                            PaymentCart = %s,
                            OtherExpenses = %s,
                            OtherExpense1Desc = %s,
                            OtherExpense1Amount = %s,
                            OtherExpense2Desc = %s,
                            OtherExpense2Amount = %s,
                            OtherExpense3Desc = %s,
                            OtherExpense3Amount = %s,
                            OtherExpense4Desc = %s,
                            OtherExpense4Amount = %s,
                            OtherExpense5Desc = %s,
                            OtherExpense5Amount = %s
                            WHERE Month = %s AND Year = %s;
                            """
            all_data = [Electricity, InternetBills, OfficeCleaner, ZoomCharge, Publication, Antivirus, toner, MSWord, Domain, SundryOthers, PlantMaintenance, PostCourier, OfficeSupply, Businesscard, TrainingEmployee, AnnualParty, ACMaintenance, PolycomCable, SundryOther1Desc, SundryOther1Amount, SundryOther2Desc, SundryOther2Amount, SundryOther3Desc, SundryOther3Amount, SundryOther4Desc, SundryOther4Amount, SundryOther5Desc, SundryOther5Amount, IndustryReports, DirectorAccomodation, EventExpense1Desc, EventExpense1Amount, EventExpense2Desc, EventExpense2Amount, EventExpense3Desc, EventExpense3Amount, EventExpense4Desc, EventExpense4Amount, ClientLunch, HotelCost, MIODMembership, RatingFees, DirectorFees , LegalOther1Desc, LegalOther1Amount, LegalOther2Desc, LegalOther2Amount, LegalOther3Desc, LegalOther3Amount, LegalOther4Desc, LegalOther4Amount, LegalOther5Desc, LegalOther5Amount, salary, utilities, sundry, marketing, regulatory, audit, secretarial, travel, businessMAU, businessKEN, communication, insurance, depreciation, legal, bank, wellfare, head, royalty, amortisation, finance, cart, other, OtherExpense1Desc, OtherExpense1Amount, OtherExpense2Desc, OtherExpense2Amount, OtherExpense3Desc, OtherExpense3Amount, OtherExpense4Desc, OtherExpense4Amount, OtherExpense5Desc, OtherExpense5Amount, month, year]
            cursor.execute(update_all, all_data)
            print("All Expense Updated")

            update_data = """UPDATE expenses
                            SET
                            salary = %s,
                            rent = %s,
                            utilities = %s,
                            sundry = %s,
                            marketing = %s,
                            regulatory = %s,
                            audit = %s,
                            secretarial = %s,
                            travel = %s,
                            businessMAU = %s,
                            businessKEN = %s,
                            communication = %s,
                            insurance = %s,
                            depreciation = %s,
                            legal = %s,
                            bank = %s,
                            wellfare = %s,
                            headOffice = %s,
                            royalty = %s,
                            amortisation = %s,
                            finance = %s,
                            cart = %s,
                            other = %s,
                            OtherExpense1 = %s,
                            OtherExpense2 = %s,
                            OtherExpense3 = %s,
                            OtherExpense4 = %s,
                            OtherExpense5 = %s,
                            total = %s
                            WHERE month = %s AND year = %s; 
                            """
            data = [salary, rent, utilities, sundry, marketing, regulatory, audit, secretarial, travel, businessMAU, businessKEN, communication, insurance, depreciation, legal, bank, wellfare, head, royalty, amortisation, finance, cart, other, OtherExpense1Amount, OtherExpense2Amount, OtherExpense3Amount, OtherExpense4Amount, OtherExpense5Amount , total, month, year]
            cursor.execute(update_data, data)
            print("Expense Updated")

            msg = "Expense Updated Successfully"
            return render_template("expense.html", msg=msg)

        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")   
        

    else:
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            # get_month = "SELECT DISTINCT year FROM expenses"
            # cursor.execute(get_month)
            # month_data = cursor.fetchall()

            

            get_query = "SELECT salary, utilities,sundry,marketing,regulatory,audit,secretarial,travel,businessMAU,businessKEN,communication,insurance,depreciation,legal,bank,wellfare,headOffice,royalty,amortisation,finance,cart,other, OtherExpense1, OtherExpense2, OtherExpense3 , OtherExpense4, OtherExpense5, total FROM expenses ORDER BY monthDigit"
            cursor.execute(get_query)
            get_data = cursor.fetchall()

            get_month = "SELECT month FROM expenses ORDER BY monthDigit"
            cursor.execute(get_month)
            month_data = cursor.fetchall()

            print(month_data)

            if month_data == []:
                mon_length = 0
            else:
                mon_length = len(month_data[0])

            print(month_data)
            print(len(month_data))
            # print(len(month_data[0]))

            print(get_data)
            length = len(get_data)
            print("length ", length)

            return render_template("expensesheet.html", data = get_data, length = length, length2 = mon_length, data2 = month_data)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template("expensesheet.html")
    # return render_template("expensesheet.html")


@app.route("/revenue", methods = ["POST" , "GET"])
def revenue():       

    if request.method == "POST" and request.form["action"] == "summary":

        return render_template("revenue.html")

    elif request.method == "POST" and request.form["action"] == "summarySheet":

        from_date = request.form["FromDate"]
        if from_date == "":
            from_date = "0000-00-00"

        to_date = request.form["ToDate"]
        if to_date == "":
            to_date = "0000-00-00"

        company = request.form["company"]
        if company == "":
            company = " "
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            if from_date != "0000-00-00":
                get_query = "SELECT date, location, mandate, company, sector, products, facility, typeFees, fees, VAT, totalFees, PaymentStatus, ExecutionStatus, surveillanceFees FROM revenue WHERE date >= %s AND date <= %s"
                data = [from_date, to_date]
            else:
                get_query = "SELECT date, location, mandate, company, sector, products, facility, typeFees, fees, VAT, totalFees, PaymentStatus, ExecutionStatus, surveillanceFees FROM revenue WHERE company = %s"
                data = [company]
            
            cursor.execute(get_query, data)
            get_data = cursor.fetchall()

            print(get_data)

            return render_template("revenuesheet.html", data = get_data)

        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            # print(get_data)
        
        return render_template("revenuesheet.html")
        
    elif request.method == "POST" and request.form["action"] == "input":
        return render_template("revenue2.html")
    
    elif request.method == "POST" and request.form["action"] == "find":
        print("IN Find")
        return render_template("revenueFind.html")

    elif request.method == "POST" and request.form["action"] == "findData":
        print("IN Find Data")
        company = request.form["company"]
        mandate = request.form["mandate"]
        data_date = request.form["date1"]
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            get_query = "SELECT date, location, mandate, company, sector, products, facility, typeFees, fees, VAT, totalFees , PaymentStatus, ExecutionStatus, surveillanceFees, paymentDate, RCMDate, invoiceNumber FROM revenue WHERE company = %s AND mandate = %s AND date = %s"
            data = [company, mandate, data_date]
            cursor.execute(get_query, data)
            get_data = cursor.fetchall()

            print(get_data)
            length = len(get_data)

            return render_template("revenueData.html", data = get_data, length = length)

        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return render_template("revenueData.html")

    elif request.method == "POST" and request.form["action"] == "save":
        
        company = request.form["company"]
        mandate = request.form["mandate"]
        date = request.form["date1"]
        if date == "":
            date = "0001-01-01"

        location = request.form["location"]
        sector = request.form["sector"]
        
        # company_type = request.form["type"]
        # company_type = ""
        products = request.form["products"]
        
        # facility = request.form["facility"]
        FacilityAmount = request.form["amount"]
        if FacilityAmount == "":
            FacilityAmount = 0

        TypeFees = request.form["typeFees"]
        if TypeFees == "":
            TypeFees = 0

        Fees = request.form["fees"]
        if Fees == "":
            Fees = 0

        VAT = request.form["VAT"]
        print(VAT)
        # if VAT == "0":
        #     print("In If")
        #     VAT = "0%"

        print(VAT)

        total_fees = request.form["totalfee"]
        if total_fees == "":
            total_fees = 0 

        payment_status = request.form["pay"]
        if payment_status == "":
            payment_status = " "

        execution_status = request.form["execution"]
        if execution_status == "":
            execution_status = " "

        SurveillanceFees = request.form["sur"]
        if SurveillanceFees == "":
            SurveillanceFees = 0
        
        paymentDate = request.form["payDate"]
        if paymentDate == "":
            paymentDate = "0001-01-01"

        RCMDate = request.form["RCM"]
        if RCMDate == "":
            RCMDate = "0001-01-01"

        invoiceNumber = request.form["invoiceNumber"]
        if invoiceNumber == "":
            invoiceNumber = " "

        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)
            
            insert_query = """INSERT INTO revenue(
                            date,
                            location,
                            mandate,
                            company,
                            sector,
                            products,
                            facility,
                            typeFees,
                            fees,
                            VAT,
                            totalFees,
                            invoiceNumber,
                            PaymentStatus,
                            paymentDate,
                            ExecutionStatus,
                            RCMDate,
                            surveillanceFees
                            )
                            VALUES
                            (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                            );
                            """
            data = [date, location, mandate, company, sector, products, FacilityAmount, TypeFees, Fees, VAT, total_fees, invoiceNumber , payment_status, paymentDate , execution_status, RCMDate , SurveillanceFees]
            cursor.execute(insert_query, data)
            print("Insert Query Executed")
            msg = "Revenue Added"

            return render_template("revenue2.html", msg=msg)

        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

        return render_template("revenue2.html")

    elif request.method == "POST" and request.form["action"] == "update":
        
        company = request.form["company"]
        company2 = request.form["company2"]
        if company2 == "":
            company2 = company

        mandate = request.form["mandate"]
        mandate2 = request.form["mandate2"]
        if mandate2 == "":
            mandate2 = mandate
        
        date = request.form["date1"]
        if date == "":
            date = "0001-01-01"
        
        date2 = request.form["date2"]
        if date2 == "":
            date2 = date

        location = request.form["location"]
        sector = request.form["sector"]
        
        # company_type = request.form["type"]
        # company_type = ""
        products = request.form["products"]
        
        # facility = request.form["facility"]
        FacilityAmount = request.form["amount"]
        if FacilityAmount == "":
            FacilityAmount = 0

        TypeFees = request.form["typeFees"]
        if TypeFees == "":
            TypeFees = 0

        Fees = request.form["fees"]
        if Fees == "":
            Fees = 0

        VAT = request.form["VAT"]
        print(VAT)
        # if VAT == "0":
        #     print("In If")
        #     VAT = "0%"

        print(VAT)

        total_fees = request.form["totalfee"]
        if total_fees == "":
            total_fees = 0 

        payment_status = request.form["pay"]
        if payment_status == "":
            payment_status = " "

        execution_status = request.form["execution"]
        if execution_status == "":
            execution_status = " "

        SurveillanceFees = request.form["sur"]
        if SurveillanceFees == "":
            SurveillanceFees = 0
        
        paymentDate = request.form["payDate"]
        if paymentDate == "":
            paymentDate = "0001-01-01"

        RCMDate = request.form["RCM"]
        if RCMDate == "":
            RCMDate = "0001-01-01"

        invoiceNumber = request.form["invoiceNumber"]
        if invoiceNumber == "":
            invoiceNumber = " "

        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            update_query = """UPDATE revenue
                            SET
                            date = %s,
                            location =%s,
                            mandate = %s,
                            company = %s,
                            sector = %s,
                            products = %s,
                            facility = %s,
                            typeFees = %s,
                            fees = %s,
                            VAT =%s,
                            totalFees = %s,
                            invoiceNumber = %s,
                            PaymentStatus = %s,
                            paymentDate = %s,
                            ExecutionStatus = %s,
                            RCMDate = %s,
                            surveillanceFees = %s
                            WHERE company = %s AND mandate = %s and date = %s;
                            """
            data = [date2, location, mandate2, company2, sector, products, FacilityAmount, TypeFees, Fees, VAT, total_fees, invoiceNumber , payment_status, paymentDate , execution_status, RCMDate , SurveillanceFees, company, mandate, date]
            cursor.execute(update_query, data)

            msg = "Revenue Updated Successfully "

            return render_template("revenue2.html", msg=msg)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

        

    else:
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            get_query = "SELECT date, location, mandate, company, sector, products, facility, typeFees, fees, VAT, totalfees, PaymentStatus, ExecutionStatus, surveillanceFees FROM revenue"
            cursor.execute(get_query)
            get_data = cursor.fetchall()

            print(get_data)



            return render_template("revenuesheet.html", data = get_data)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template("revenuesheet.html")


@app.route("/rae", methods=["POST" , "GET"])
def rae():
    print("In RAE")
    if request.method == "POST" and request.form['action'] == 'expense':
        return redirect(url_for('expense'))
    if request.method == "POST" and request.form['action'] == 'revenue':
        return redirect(url_for('revenue'))
    if request.method == "POST" and request.form['action'] == 'main':
        return render_template("module.html")
    
    return render_template("module2.html")


@app.route("/module", methods=["GET", "POST"])
def module():
    if request.method == "POST" and request.form['action'] == 'payroll':
        value = request.form['action']
        print("User Choose Payroll Module - Goes To Password Page")
        print(value)
        return render_template("password.html", value = value)

# ===================================================================================================

    if request.method == "POST" and request.form['action'] == 'rae':  #Revenue And Expense (RAE)
        print("User Choose Revenue & Expense Module - Goes To Expense And Revenue Page")
        return redirect(url_for('rae'))

    if request.method == "POST" and request.form['action'] == 'home':
        print("In Logout")
        return render_template("login.html")
    return render_template("module.html")


@app.route('/contribution', methods=["POST", "GET"])
def contribution():
    if request.method == "POST" and request.form['action'] == 'contri':
        mon = request.form["mon"]
        year = request.form["year"]
        data = [mon]

        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            data2 = [year]
            for i in range(len(data)):
                month = ' '.join(data[i])

            for i in range(len(data2)):
                year = ' '.join(data2[i])

            query = "SELECT EmployeeID, LastName, FirstName, IDCard, Salary, blank1, ecsg, elevy, ensf, prgf, csg, nsf, slevy, paye FROM contribution WHERE month = %s"

            cursor.execute(query,data)
            contri_data = cursor.fetchall()

            length = len(contri_data)

            query2 = "SELECT totalRem FROM contribution WHERE month = %s"
            cursor.execute(query2, data)
            totalRem = cursor.fetchall()
            print(totalRem)

            if totalRem == []:
                totalRem = 0
            else:
                totalRem = totalRem[0][0]

            query3 = "SELECT totalecsg FROM contribution WHERE month = %s"
            cursor.execute(query3, data)
            totalecsg = cursor.fetchall()

            if totalecsg == []:
                totalecsg = 0
            else:
                totalecsg = totalecsg[0][0]

            query4 = "SELECT totalelevy FROM contribution WHERE month = %s"
            cursor.execute(query4, data)
            totalelevy = cursor.fetchall()

            if totalelevy == []:
                totalelevy = 0
            else:
                totalelevy = totalelevy[0][0]

            query5 = "SELECT totalensf FROM contribution WHERE month = %s"
            cursor.execute(query5, data)
            totalensf = cursor.fetchall()

            if totalensf == []:
                totalensf = 0
            else:
                totalensf = totalensf[0][0]

            # totalensf = totalensf[0][0]

            query6 = "SELECT totalcsg FROM contribution WHERE month = %s"
            cursor.execute(query6, data)
            totalcsg = cursor.fetchall()

            if totalcsg == []:
                totalcsg = 0
            else:
                totalcsg = totalcsg[0][0]

            query7 = "SELECT totalnsf FROM contribution WHERE month = %s"
            cursor.execute(query7, data)
            totalnsf = cursor.fetchall()

            if totalnsf == []:
                totalnsf = 0
            else:
                totalnsf = totalnsf[0][0]

            query8 = "SELECT totalslevy FROM contribution WHERE month = %s"
            cursor.execute(query8, data)
            totalslevy = cursor.fetchall()

            if totalslevy == []:
                totalslevy = 0
            else:
                totalslevy = totalslevy[0][0]

            query9 = "SELECT totalprgf FROM contribution WHERE month = %s"
            cursor.execute(query9, data)
            totalprgf = cursor.fetchall()

            if totalprgf == []:
                totalprgf = 0
            else:
                totalprgf = totalprgf[0][0]

            query10 = "SELECT totalpaye FROM contribution WHERE month = %s"
            cursor.execute(query10, data)
            totalpaye = cursor.fetchall()

            if totalpaye == []:
                totalpaye = 0
            else:
                totalpaye = totalpaye[0][0]

            
            return render_template("contribution2.html", length = length, data= contri_data, month = month, year = year, totalRem = totalRem, totalecsg = totalecsg, totalelevy = totalelevy, totalensf = totalensf, totalcsg = totalcsg,totalnsf = totalnsf, totalslevy = totalslevy , totalprgf = totalprgf, totalpaye = totalpaye)

        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")        

    return render_template("contribution.html")


@app.route("/reset", methods=["GET","POST"])
def reset():
    # global connection
    if request.method == "POST":
        old_pass = request.form["opass"]
        new_pass = request.form["npass"]
        rnew_pass = request.form["rpass"]
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            query1 = "SELECT password FROM cred"
            cursor.execute(query1)
            password = cursor.fetchall()
            password = password[0][0]

            plaintext = old_pass.encode()
            d = hashlib.md5(plaintext)
            hash = d.hexdigest()

            if password == hash:
                if new_pass == rnew_pass:
                    query2 = """UPDATE cred
                    SET
                    password = %s
                    WHERE
                    username= %s
                    """
                    plaintext2 = new_pass.encode()
                    d = hashlib.md5(plaintext2)
                    hash2 = d.hexdigest()

                    data = [hash2,"admin"]
                    cursor.execute(query2,data)
                    msg = "Password updated Successfully"
                    return render_template("login.html", msg=msg)
                else:
                    msg = "New password and Re-Enter Password not match"
                    return render_template("reset.html", msg=msg)
            else:
                msg = "Old Password Wrong"
                return render_template("reset.html", msg=msg)

        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template("reset.html")

@app.route("/dashboard", methods=["GET" , "POST"])
def dashboard():
    print("In Dashboard Without Post method")
    # global connection
    if request.method == "POST":
        print("In Dashboard with Post method before If")
        eid = request.form["search"]
        if eid:
            data1 = [eid]
            print("In If")
            try:
                connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
                cursor = connection.cursor(buffered=True)
                
                query2 = "SELECT EmployeeID, FirstName, LastName, working FROM employee WHERE EmployeeID = %s "
                cursor.execute(query2, data1)
                table_data = cursor.fetchall()
                print(table_data)
                return render_template("dashboard.html", data = table_data)

            except Error as e:
                    print("Error While connecting to MySQL : ", e)
            finally:
                connection.commit()
                cursor.close()
                connection.close()
                print("MySQL connection is closed")                   

    else:
        print("In Else")
        # eid = request.form["search"]
        # data1 = [eid]
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True) 

            # query1 = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'employee'"
            # cursor.execute(query1)
            # column_name = cursor.fetchall()

            print("Before Query1")
            query1 = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'employee' AND COLUMN_NAME = 'EmployeeID' OR COLUMN_NAME = 'working' OR COLUMN_NAME = 'FirstName' OR COLUMN_NAME = 'LastName';"
            # query1 = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'employee' AND ORDINAL_POSITION between 2 AND 4;"
            cursor.execute(query1)
            print("Query1 Executed")
            column_name = cursor.fetchall()
            heading_data = []
            data = []
            print(len(column_name))
            for i in range(len(column_name)):
                print("i : " , i)
                # print("j : ", j)
                data = ''.join(column_name[i])
                print("Data :" + data)
                heading_data.append(data)
            
            print(column_name)
            print(heading_data)

            # query2 = "SELECT EmployeeID, FirstName, LastName FROM employee WHERE EmployeeID = %s "
            # query2 = "SELECT EmployeeID, FirstName, LastName FROM employee WHERE FirstName = %s "
            # query2 = "SELECT EmployeeID, FirstName, LastName FROM employee WHERE LastName = %s "
            # query2 = "SELECT EmployeeID, FirstName, LastName FROM employee WHERE position = %s "
            # query2 = f"SELECT EmployeeID, FirstName, LastName FROM employee"
            query2 = "SELECT EmployeeID, FirstName, LastName, working FROM employee"
            cursor.execute(query2)
            table_data = cursor.fetchall()

            print(table_data)
            return render_template("dashboard.html", heading = heading_data, data = table_data)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    print("Before Return")
    return render_template("dashboard.html")

@app.route("/employee", methods=["GET" , "POST"])
def employee():
    # global connection
    # Back To Employee Page

    if request.method == "POST" and request.form['action'] == 'back':      
        return render_template("employee.html")

    # Fetch Data

    if request.method == "POST" and request.form['action'] == 'search2': 
        
        lname = request.form["lname"]
        fname = request.form["fname"]
        position = request.form["pos"]
        eid = request.form["eid"]

        if eid:
            return render_template("dashboard.html", eid=eid)
        
# ==========================================================================================================        

    # Search Employee Page
    if request.method == "POST" and request.form['action'] == 'search':
        eid = request.form["eid"]      
        data = [eid]
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)
            
            query1 = "SELECT FirstName From employee WHERE EmployeeID = %s"
            cursor.execute(query1, data)
            fname = cursor.fetchall()
            for i in range(len(fname)):
                fname = ''.join(fname[i])

            query2 = "SELECT LastName From employee WHERE EmployeeID = %s"
            cursor.execute(query2, data)
            lname = cursor.fetchall()
            for i in range(len(lname)):
                lname = ''.join(lname[i])
            
            query3 = "SELECT Title From employee WHERE EmployeeID = %s"
            cursor.execute(query3, data)
            title = cursor.fetchall()
            for i in range(len(title)):
                title = ''.join(title[i])

            query4 = "SELECT DOB From employee WHERE EmployeeID = %s"
            cursor.execute(query4, data)
            dob = cursor.fetchall()
            print(dob)
            if dob == []:
                dob = "0001-01-01"
            else:
                dob = dob[0][0]

            query5 = "SELECT address From employee WHERE EmployeeID = %s"
            cursor.execute(query5, data)
            add = cursor.fetchall()
            for i in range(len(add)):
                add = ''.join(add[i])

            query6 = "SELECT city From employee WHERE EmployeeID = %s"
            cursor.execute(query6, data)
            city = cursor.fetchall()
            for i in range(len(city)):
                city = ''.join(city[i])

            query7 = "SELECT country From employee WHERE EmployeeID = %s"
            cursor.execute(query7, data)
            country = cursor.fetchall()
            for i in range(len(country)):
                country = ''.join(country[i])

            query8 = "SELECT phone From employee WHERE EmployeeID = %s"
            cursor.execute(query8, data)
            phone = cursor.fetchall()
            for i in range(len(phone)):
                phone = ''.join(phone[i])

            query9 = "SELECT mobile From employee WHERE EmployeeID = %s"
            cursor.execute(query9, data)
            mobile = cursor.fetchall()
            for i in range(len(mobile)):
                mobile = ''.join(mobile[i])

            query10 = "SELECT fax From employee WHERE EmployeeID = %s"
            cursor.execute(query10, data)
            fax = cursor.fetchall()
            for i in range(len(fax)):
                fax = ''.join(fax[i])

            query11 = "SELECT email From employee WHERE EmployeeID = %s"
            cursor.execute(query11, data)
            mail = cursor.fetchall()
            for i in range(len(mail)):
                mail = ''.join(mail[i])

            query12 = "SELECT NICno From employee WHERE EmployeeID = %s"
            cursor.execute(query12, data)
            nic = cursor.fetchall()
            for i in range(len(nic)):
                nic = ''.join(nic[i])

            query13 = "SELECT TaxAC From employee WHERE EmployeeID = %s"
            cursor.execute(query13, data)
            tax = cursor.fetchall()
            for i in range(len(tax)):
                tax = ''.join(tax[i])

            query14 = "SELECT Bank From employee WHERE EmployeeID = %s"
            cursor.execute(query14, data)
            bank = cursor.fetchall()
            for i in range(len(bank)):
                bank = ''.join(bank[i])

            query15 = "SELECT BankAC From employee WHERE EmployeeID = %s"
            cursor.execute(query15, data)
            bankac = cursor.fetchall()
            for i in range(len(bankac)):
                bankac = ''.join(bankac[i])

            query16 = "SELECT Bankcode From employee WHERE EmployeeID = %s"
            cursor.execute(query16, data)
            code = cursor.fetchall()
            for i in range(len(code)):
                code = ''.join(code[i])
            
            query17 = "SELECT Carbenefit From employee WHERE EmployeeID = %s"
            cursor.execute(query17, data)
            car = cursor.fetchall()
            for i in range(len(car)):
                car = ''.join(car[i])
            
            query18 = "SELECT hire From employee WHERE EmployeeID = %s"
            cursor.execute(query18, data)
            hire = cursor.fetchall()
            if hire == []:
                hire = "0001-01-01"
            else:
                hire = hire[0][0]

            query19 = "SELECT salary From employee WHERE EmployeeID = %s"
            cursor.execute(query19, data)
            salary = cursor.fetchall()
            for i in range(len(salary)):
                salary = ''.join(salary[i])

            query20 = "SELECT position From employee WHERE EmployeeID = %s"
            cursor.execute(query20, data)
            position = cursor.fetchall()
            for i in range(len(position)):
                position = ''.join(position[i])
            
            query21 = "SELECT department From employee WHERE EmployeeID = %s"
            cursor.execute(query21, data)
            dep = cursor.fetchall()
            for i in range(len(dep)):
                dep = ''.join(dep[i])

            query22 = "SELECT Subdepartment From employee WHERE EmployeeID = %s"
            cursor.execute(query22, data)
            sdep = cursor.fetchall()
            for i in range(len(sdep)):
                sdep = ''.join(sdep[i])

            query23 = "SELECT Payescheme From employee WHERE EmployeeID = %s"
            cursor.execute(query23, data)
            payes = cursor.fetchall()
            for i in range(len(payes)):
                payes = ''.join(payes[i])

            query24 = "SELECT Payepercentage From employee WHERE EmployeeID = %s"
            cursor.execute(query24, data)
            payep = cursor.fetchall()
            for i in range(len(payep)):
                payep = ''.join(payep[i])

            query25 = "SELECT Localleave From employee WHERE EmployeeID = %s"
            cursor.execute(query25, data)
            lleave = cursor.fetchall()
            for i in range(len(lleave)):
                lleave = ''.join(lleave[i])

            query26 = "SELECT Sickleave From employee WHERE EmployeeID = %s"
            cursor.execute(query26, data)
            sleave = cursor.fetchall()
            for i in range(len(sleave)):
                sleave = ''.join(sleave[i])

            query27 = "SELECT Fixedallow From employee WHERE EmployeeID = %s"
            cursor.execute(query27, data)
            falw = cursor.fetchall()
            for i in range(len(falw)):
                falw = ''.join(falw[i])

            query28 = "SELECT Travelmode From employee WHERE EmployeeID = %s"
            cursor.execute(query28, data)
            travelmod = cursor.fetchall()
            for i in range(len(travelmod)):
                travelmod = ''.join(travelmod[i])

            query29 = "SELECT Travelallow From employee WHERE EmployeeID = %s"
            cursor.execute(query29, data)
            talw = cursor.fetchall()
            for i in range(len(talw)):
                talw = ''.join(talw[i])

            query30 = "SELECT EDF From employee WHERE EmployeeID = %s"
            cursor.execute(query30, data)
            edf = cursor.fetchall()
            for i in range(len(edf)):
                edf = ''.join(edf[i])

            query31 = "SELECT months From employee WHERE EmployeeID = %s"
            cursor.execute(query31, data)
            mon = cursor.fetchall()
            for i in range(len(mon)):
                mon = ''.join(mon[i])

            query32 = "SELECT MonthlyEDF From employee WHERE EmployeeID = %s"
            cursor.execute(query32, data)
            medf = cursor.fetchall()
            for i in range(len(medf)):
                medf = ''.join(medf[i])

            query33 = "SELECT Houseinterest From employee WHERE EmployeeID = %s"
            cursor.execute(query33, data)
            house = cursor.fetchall()
            for i in range(len(house)):
                house = ''.join(house[i])

            query34 = "SELECT Educationrel From employee WHERE EmployeeID = %s"
            cursor.execute(query34, data)
            erel = cursor.fetchall()
            for i in range(len(erel)):
                erel = ''.join(erel[i])

            query35 = "SELECT Medicalrel From employee WHERE EmployeeID = %s"
            cursor.execute(query35, data)
            mrel = cursor.fetchall()
            for i in range(len(mrel)):
                mrel = ''.join(mrel[i])

            query36 = "SELECT Paymentmode From employee WHERE EmployeeID = %s"
            cursor.execute(query36, data)
            pay = cursor.fetchall()
            for i in range(len(pay)):
                pay = ''.join(pay[i])

            query37 = "SELECT medical From employee WHERE EmployeeID = %s"
            cursor.execute(query37, data)
            med = cursor.fetchall()
            for i in range(len(med)):
                med = ''.join(med[i])

            query38 = "SELECT Specialbonus From employee WHERE EmployeeID = %s"
            cursor.execute(query38, data)
            spbns = cursor.fetchall()
            for i in range(len(spbns)):
                spbns = ''.join(spbns[i])

            query39 = "SELECT Workingdays From employee WHERE EmployeeID = %s"
            cursor.execute(query39, data)
            work = cursor.fetchall()
            for i in range(len(work)):
                work = ''.join(work[i])

            query40 = "SELECT Lastwork From employee WHERE EmployeeID = %s"
            cursor.execute(query40, data)
            last = cursor.fetchall()
            print(last)
            if last == []:
                last = "0001-01-01"
            else:
                last = last[0][0]

            query41 = "SELECT working From employee WHERE EmployeeID = %s"
            cursor.execute(query41, data)
            working = cursor.fetchall()
            for i in range(len(working)):
                working = ''.join(working[i])
            
            query42 = "SELECT NPS From employee WHERE EmployeeID = %s"
            cursor.execute(query42, data)
            pension = cursor.fetchall()
            for i in range(len(pension)):
                pension = ''.join(pension[i])

            print(pension)

            query43 = "SELECT expatriate From employee WHERE EmployeeID = %s"
            cursor.execute(query43, data)
            exp = cursor.fetchall()
            print(exp)
            for i in range(len(exp)):
                exp = ''.join(exp[i])


            return render_template("employee2.html",eid=eid, fname=fname, lname=lname, title=title,dob=dob, add=add, city=city, country=country, phone=phone, mobile=mobile, fax=fax, mail=mail, nic=nic, tax=tax, bank=bank, bankac =bankac,code=code, car=car, hire=hire, salary=salary, position=position, dep=dep, sdep=sdep, payes=payes, payep=payep, lleave=lleave, sleave=sleave, falw=falw, travelmod = travelmod, talw=talw, edf=edf, mon=mon, medf=medf, house=house, erel=erel, mrel=mrel, pay=pay, med=med, spbns=spbns, work=work , last=last, working = working, pension = pension, exp=exp)

        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return render_template("employee.html") 

# ==========================================================================================================

    # Update To Database

    if request.method == "POST" and request.form['action']== 'update':
        eid = request.form["eid"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        title = request.form["title"]
        dob = request.form["dob"]
        clocked = request.form["optradio"]
        address = request.form["add"]
        city = request.form["city"]
        country = request.form["con"]
        phone = request.form["phn"]
        mobile = request.form["mob"]
        fax = request.form["fax"]
        mail = request.form["mail"]
        if request.files["img"]:
            eimage = request.files["img"]
        else:
            eimage = ""
        nic = request.form["nic"]
        tax = request.form["tax"]
        bank = request.form["bank"]
        bank_ac = request.form["bac"]
        code = request.form["code"]
        # report = request.form["rpt"]
        report = ""
        nps = request.form["optradio2"]
        car = request.form["car"]
        hire = request.form["hire"]
        salary = request.form["sal"]
        position = request.form["pos"]
        dep = request.form["dep"]
        # sdep = request.form["sdep"]
        sdep = ""
        paye = request.form["psch"]
        per = request.form["per"]
        lleave = request.form["lleave"]
        sleave = request.form["sleave"]
        fallow = request.form["falw"]
        tmode = request.form["tmode"]
        tallow = request.form["talw"]
        expatriate = request.form["optradio4"]
        edf = request.form["edf"]
        months = request.form["month"]  
        medf = request.form["medf"]
        house = request.form["hint"]
        erel = request.form["erel"]
        mrel = request.form["mrel"]
        payment = request.form["optradio5"]
        medical = request.form["med"]
        working = request.form["optradio3"]
        if working == "No":
            lwork = request.form["lwork"]
        else:
            lwork = "0001-01-01"
        spbonus = request.form["spbonus"]
        wdays = request.form["wday"]

        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            update_query = """
            UPDATE employee
            SET
            FirstName =%s ,
            LastName =%s ,
            Title =%s ,
            DOB =%s ,
            address =%s ,
            city =%s ,
            country =%s ,
            phone =%s ,
            mobile =%s ,
            fax =%s ,
            email =%s ,
            NICno =%s ,
            TaxAC =%s ,
            Bank =%s ,
            BankAC =%s ,
            Bankcode =%s ,
            NPS = %s,
            Carbenefit =%s ,
            hire =%s ,
            salary =%s ,
            position =%s ,
            department =%s ,
            Subdepartment =%s ,
            Payescheme =%s ,
            Payepercentage =%s ,
            Localleave =%s ,
            Sickleave =%s ,
            Fixedallow =%s ,
            Travelmode =%s ,
            Travelallow =%s ,
            expatriate =%s ,
            EDF =%s ,
            months =%s ,
            MonthlyEDF =%s ,
            Houseinterest =%s ,
            Educationrel =%s ,
            Medicalrel =%s ,
            Paymentmode =%s ,
            medical =%s ,
            working =%s ,
            Lastwork =%s ,
            Specialbonus =%s ,
            Workingdays = %s
            WHERE
            EmployeeID = %s;
            """

            data = [fname, lname, title, dob, address, city, country, phone, mobile, fax, mail, nic, tax, bank, bank_ac, code, nps, car, hire, salary, position, dep, sdep, paye, per, lleave, sleave, fallow, tmode, tallow, expatriate, edf, months, medf, house, erel, mrel, payment, medical, working, lwork, spbonus, wdays, eid]
            print("Before Update")

            cursor.execute(update_query, data)

            print("After Update")

            msg = "Update Successfully"
            return render_template("employee.html", msg=msg)    
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return render_template("employee.html")         
# ==========================================================================================================

# Redirect

    if request.method == "POST" and request.form['action']== 'redirect':
        eid = request.form["eid"]
        return render_template("change_id.html", eid=eid)

# Change Username
    if request.method == "POST" and request.form['action']== 'change':
        eid1 = request.form["eid1"]
        eid2 = request.form["eid2"]
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                database='defaultdb',
                                                user='doadmin',
                                                port='25060',
                                                password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            query1 = "SELECT EmployeeID FROM employee WHERE EmployeeID=%s"
            data1 = [eid1]
            cursor.execute(query1, data1)

            eid = cursor.fetchall()
            for i in range(len(eid)):
                eid = ''.join(eid[i])
            
            if eid == eid1:
                update_query = """UPDATE employee
                            SET
                            EmployeeID = %s
                            WHERE
                            EmployeeID = %s;
                            """
                data = [eid2, eid1]
                cursor.execute(update_query, data)
                print("Data Updated Successfully")
                msg = "Data Updated Successfully"
                return render_template("employee.html", msg=msg)
            else:
                msg = "Employee ID Not Available"
                return render_template("change_id.html", msg=msg)
            
        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        
        return render_template("change_id.html")

    


# ==========================================================================================================
    # Save To Database

    if request.method == "POST" and request.form['action']== 'save':
        print("in Save")
        eid = request.form["eid"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        title = request.form["title"]
        dob = request.form["dob"]
        print("dob ", dob)
        if dob == "":
            dob = "0001-01-01"
        else:
            dob = dob
        print("dob ", dob)
        clocked = request.form["optradio"]
        address = request.form["add"]
        city = request.form["city"]
        country = request.form["con"]
        phone = request.form["phn"]
        mobile = request.form["mob"]
        fax = request.form["fax"]
        mail = request.form["mail"]
        if request.files["img"]:
            eimage = request.files["img"]
        else:
            eimage = ""
        nic = request.form["nic"]
        tax = request.form["tax"]
        bank = request.form["bank"]
        bank_ac = request.form["bac"]
        code = request.form["code"]
        # report = request.form["rpt"]
        report = ""
        nps = request.form["optradio2"]
        car = request.form["car"]
        print(car)
        if car == "":
            print("In If")
            car = "0"
        else:
            print("In Else")
            car = car
        hire = request.form["hire"]
        if hire == "":
            hire = "0001-01-01"
        else:
            hire = hire
        
        salary = request.form["sal"]
        if salary == "":
            salary = "0"
        else:
            salary == salary

        position = request.form["pos"]
        dep = request.form["dep"]
        # sdep = request.form["sdep"]
        sdep = ""
        paye = request.form["psch"]
        per = request.form["per"]

        lleave = request.form["lleave"]
        if lleave == "":
            lleave = "0"
        else:
            lleave == lleave

        sleave = request.form["sleave"]
        if sleave == "":
            sleave = "0"
        else:
            sleave == sleave

        fallow = request.form["falw"]
        if fallow == "":
            fallow = "0"
        else:
            fallow == fallow

        tmode = request.form["tmode"]
        tallow = request.form["talw"]
        if tallow == "":
            tallow = "0"
        else:
            tallow == tallow

        expatriate = request.form["optradiod4"]
        print("expatriate " , expatriate)

        edf = request.form["edf"]
        if edf == "":
            edf = "0"
        else:
            edf == edf

        months = request.form["month"]  
        medf = request.form["medf"]
        house = request.form["hint"]
        if house == "":
            house = "0"
        else:
            house == house

        erel = request.form["erel"]
        if erel == "":
            erel = "0"
        else:
            erel == erel

        mrel = request.form["mrel"]
        if mrel == "":
            mrel = "0"
        else:
            mrel == mrel

        payment = request.form["optradio5"]
        medical = request.form["med"]
        working = request.form["optradio3"]
        if working == "No":
            lwork = request.form["lwork"]
        else:
            lwork = "0001-01-01"
        spbonus = request.form["spbonus"]
        if spbonus == "":
            spbonus = "0"
        else:
            spbonus == spbonus

        wdays = request.form["wday"]
        if wdays == "":
            wdays = "0"
        else:
            wdays == wdays

        

        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)
            query2 =""" INSERT INTO employee (
                EmployeeID,
                FirstName,
                LastName,
                Title,
                DOB,
                clocked,
                address,
                city,
                country,
                phone,
                mobile,
                fax,
                email,
                image,
                NICno,
                TaxAC,
                Bank,
                BankAC,
                Bankcode,
                report,
                NPS,
                Carbenefit,
                hire,
                salary,
                position,
                department,
                Subdepartment,
                Payescheme,
                Payepercentage,
                Localleave,
                Sickleave,
                Fixedallow,
                Travelmode,
                Travelallow,
                expatriate,
                EDF,
                months,
                MonthlyEDF,
                Houseinterest,
                Educationrel,
                Medicalrel,
                Paymentmode,
                medical,
                working,
                Lastwork,
                Specialbonus,
                Workingdays
              )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
              );"""
            
            if(eimage != ""):
                # image = eimage.convert('RGB')    
                if eimage and allowed_file(eimage.filename):
                    print("In Image If")
                    filename = secure_filename(eimage.filename)
                    filename=''.join(random.choices(string.ascii_lowercase +string.digits, k=20))
                    picture = Image.open(eimage)
                    picture.save(os.path.join(app.config['UPLOAD_FOLDER'],filename+'.jpeg'), "JPEG", optimize = True, quality = 30)
                    print(filename)
            else:
                filename = ""
            # data1 = [eid, fname, lname, title, dob, clocked, address, city, country, phone, mobile, fax, mail,filename, nic, tax, bank, bank_ac, code, report, nps, car, hire, salary, position, dep, sdep, paye, per, lleave, sleave, fallow, tmode, tallow, expatriate, edf, months, medf, house, erel, mrel, payment, medical, working, lwork, spbonus, wdays]
            data1 = [eid, fname, lname, title, dob, clocked, address, city, country, phone, mobile, fax, mail, filename, nic, tax, bank, bank_ac, code, report, nps, car, hire, salary, position, dep, sdep, paye, per, lleave, sleave, fallow, tmode, tallow, expatriate, edf, months, medf, house, erel, mrel, payment, medical, working, lwork, spbonus, wdays]
            print("Before Query")
            cursor.execute(query2, data1)
            print("Insert Query Successfully")
            msg = "New Employee Created Successfully"
            return render_template("employee.html" , msg=msg)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template("employee.html")         

@app.route("/salary", methods=["GET" , "POST"])
def salary():
    # global connection
    # Search Data
    if request.method == "POST" and request.form['action'] == 'search':
        eid = request.form["eid"]
        month = request.form["mon"]
        year = request.form["year"]
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True) 
            
            data1 = [eid, month]
            data2 = [eid]

            query = "SELECT LockSal FROM salary WHERE EmployeeID = %s AND Month = %s"
            cursor.execute(query,data1)
            lockSal = cursor.fetchall()
            for i in range(len(lockSal)):
                lockSal = ''.join(lockSal[i])

            if lockSal == "No":

                query1 = "SELECT BasicSalary From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query1, data1)
                basic = cursor.fetchall()
                for i in range(len(basic)):
                    basic = ''.join(basic[i])

                query2 = "SELECT Fixedallow From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query2, data1)
                falw = cursor.fetchall()
                for i in range(len(falw)):
                    falw = ''.join(falw[i])

                query3 = "SELECT OtherDeduction From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query3, data1)
                otherded = cursor.fetchall()
                for i in range(len(otherded)):
                    otherded = ''.join(otherded[i])

                query4 = "SELECT Overtime From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query4, data1)
                ot = cursor.fetchall()
                for i in range(len(ot)):
                    ot = ''.join(ot[i])

                query5 = "SELECT DiscBonus From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query5, data1)
                disc = cursor.fetchall()
                for i in range(len(disc)):
                    disc = ''.join(disc[i])

                query6 = "SELECT NSFEmpee From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query6, data1)
                nsf = cursor.fetchall()
                for i in range(len(nsf)):
                    nsf = ''.join(nsf[i])

                query7 = "SELECT OtherAllow From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query7, data1)
                oalw = cursor.fetchall()
                for i in range(len(oalw)):
                    oalw = ''.join(oalw[i])

                query8 = "SELECT TaxableAllow From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query8, data1)
                tax = cursor.fetchall()
                for i in range(len(tax)):
                    tax = ''.join(tax[i])

                query9 = "SELECT Medical From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query9, data1)
                med = cursor.fetchall()
                for i in range(len(med)):
                    med = ''.join(med[i])

                query10 = "SELECT Transport From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query10, data1)
                tran = cursor.fetchall()
                for i in range(len(tran)):
                    tran = ''.join(tran[i])

                query11 = "SELECT NTaxableAllow From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query11, data1)
                ntax = cursor.fetchall()
                for i in range(len(ntax)):
                    ntax = ''.join(ntax[i])

                query12 = "SELECT EDF From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query12, data1)
                edf = cursor.fetchall()
                for i in range(len(edf)):
                    edf = ''.join(edf[i])

                query13 = "SELECT Arrears From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query13, data1)
                arr = cursor.fetchall()
                for i in range(len(arr)):
                    arr = ''.join(arr[i])

                query14 = "SELECT AttendanceBns From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query14, data1)
                att = cursor.fetchall()
                for i in range(len(att)):
                    att = ''.join(att[i])

                # query15 = "SELECT TravelAllow From OriginalData WHERE EmployeeID = %s AND Month = %s"
                # cursor.execute(query15, data1)
                # travel = cursor.fetchall()
                # for i in range(len(travel)):
                #     travel = ''.join(travel[i])

                query16 = "SELECT EOY From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query16, data1)
                eoy = cursor.fetchall()
                for i in range(len(eoy)):
                    eoy = ''.join(eoy[i])

                query17 = "SELECT Loan From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query17, data1)
                loan = cursor.fetchall()
                for i in range(len(loan)):
                    loan = ''.join(loan[i])

                query18 = "SELECT CarBenefit From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query18, data1)
                car = cursor.fetchall()
                for i in range(len(car)):
                    car = ''.join(car[i])

                query19 = "SELECT LeaveRef From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query19, data1)
                leave = cursor.fetchall()
                for i in range(len(leave)):
                    leave = ''.join(leave[i])

                query20 = "SELECT CurrentSLevy From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query20, data1)
                slevy = cursor.fetchall()
                for i in range(len(slevy)):
                    slevy = ''.join(slevy[i])

                query21 = "SELECT SpecialBns From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query21, data1)
                spebns = cursor.fetchall()
                for i in range(len(spebns)):
                    spebns = ''.join(spebns[i])

                query22 = "SELECT Lateness From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query22, data1)
                late = cursor.fetchall()
                for i in range(len(late)):
                    late = ''.join(late[i])

                query23 = "SELECT EducationRel From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query23, data1)
                edurel = cursor.fetchall()
                for i in range(len(edurel)):
                    edurel = ''.join(edurel[i])

                query24 = "SELECT SpeProBns From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query24, data1)
                speprobns = cursor.fetchall()
                for i in range(len(speprobns)):
                    speprobns = ''.join(speprobns[i])

                query25 = "SELECT NPS From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query25, data1)
                nps = cursor.fetchall()
                for i in range(len(nps)):
                    nps = ''.join(nps[i])

                query26 = "SELECT MedicalRel From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query26, data1)
                medrel = cursor.fetchall()
                for i in range(len(medrel)):
                    medrel = ''.join(medrel[i])

                query27 = "SELECT Payable From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query27, data1)
                payable = cursor.fetchall()
                for i in range(len(payable)):
                    payable = ''.join(payable[i])

                query28 = "SELECT Deduction From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query28, data1)
                ded = cursor.fetchall()
                for i in range(len(ded)):
                    ded = ''.join(ded[i])

                query29 = "SELECT NetPay From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query29, data1)
                net = cursor.fetchall()
                for i in range(len(net)):
                    net = ''.join(net[i])


                query31 = "SELECT CurrentGross From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query31, data1)
                cgross = cursor.fetchall()
                for i in range(len(cgross)):
                    cgross = ''.join(cgross[i])

                query32 = "SELECT PrevGross From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query32, data1)
                pgross = cursor.fetchall()
                for i in range(len(pgross)):
                    pgross = ''.join(pgross[i])

                query33 = "SELECT IET From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query33, data1)
                iet = cursor.fetchall()
                for i in range(len(iet)):
                    iet = ''.join(iet[i])

                query34 = "SELECT NetCh From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query34, data1)
                netch = cursor.fetchall()
                for i in range(len(netch)):
                    netch = ''.join(netch[i])

                query35 = "SELECT CurrentPAYE From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query35, data1)
                cpaye = cursor.fetchall()
                for i in range(len(cpaye)):
                    cpaye = ''.join(cpaye[i])

                query36 = "SELECT PrevPAYE From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query36, data1)
                ppaye = cursor.fetchall()
                for i in range(len(ppaye)):
                    ppaye = ''.join(ppaye[i])

                query37 = "SELECT PAYE From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query37, data1)
                paye = cursor.fetchall()
                for i in range(len(paye)):
                    paye = ''.join(paye[i])

                query38 = "SELECT eCSG From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query38, data1)
                ecsg = cursor.fetchall()
                for i in range(len(ecsg)):
                    ecsg = ''.join(ecsg[i])

                query39 = "SELECT eNSF From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query39, data1)
                ensf = cursor.fetchall()
                for i in range(len(ensf)):
                    ensf = ''.join(ensf[i])

                query40 = "SELECT eLevy From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query40, data1)
                elevy = cursor.fetchall()
                for i in range(len(elevy)):
                    elevy = ''.join(elevy[i])

                query41 = "SELECT Absences From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query41, data1)
                absence = cursor.fetchall()
                for i in range(len(absence)):
                    absence = ''.join(absence[i])

                query42 = "SELECT FirstName From employee WHERE EmployeeID = %s"
                cursor.execute(query42, data2)
                fname = cursor.fetchall()
                for i in range(len(fname)):
                    fname = ''.join(fname[i])

                query43 = "SELECT LastName From employee WHERE EmployeeID = %s"
                cursor.execute(query43, data2)
                lname = cursor.fetchall()
                for i in range(len(lname)):
                    lname = ''.join(lname[i])

                query44 = "SELECT position From employee WHERE EmployeeID = %s"
                cursor.execute(query44, data2)
                pos = cursor.fetchall()
                for i in range(len(pos)):
                    pos = ''.join(pos[i])

                query45 = "SELECT NetPaysheet From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query45, data1)
                pnet = cursor.fetchall()
                for i in range(len(pnet)):
                    pnet = ''.join(pnet[i])            
                
                query46 = "SELECT PrevIET From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query46, data1)
                piet = cursor.fetchall()
                for i in range(len(piet)):
                    piet = ''.join(piet[i])
                
                query47 = "SELECT PrevThreshold From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query47, data1)
                pthes = cursor.fetchall()
                for i in range(len(pthes)):
                    pthes = ''.join(pthes[i])

                query48 = "SELECT Threshold From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query48, data1)
                ths = cursor.fetchall()
                for i in range(len(ths)):
                    ths = ''.join(ths[i])

                query49 = "SELECT PrevSLevy From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query49, data1)
                plevy = cursor.fetchall()
                for i in range(len(plevy)):
                    plevy = ''.join(plevy[i])

                query50 = "SELECT slevyPay From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query50, data1)
                slevypay = cursor.fetchall()
                for i in range(len(slevypay)):
                    slevypay = ''.join(slevypay[i])

                query51 = "SELECT netchar From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query51, data1)
                netchar = cursor.fetchall()
                for i in range(len(netchar)):
                    netchar = ''.join(netchar[i])
                
                query52 = "SELECT PRGF From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query52, data1)
                prgf = cursor.fetchall()
                for i in range(len(prgf)):
                    prgf = ''.join(prgf[i])

                query53 = "SELECT cGrossTax From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query53, data1)
                gtax = cursor.fetchall()
                for i in range(len(gtax)):
                    gtax = ''.join(gtax[i])
                
                print("Before Query Execute")
                query54 = "SELECT Arrears, LocalRef, FixedAllowance, DiscBns, AttBns, Transport, SickRef, SpeBns, OtherAlw, Overseas, OtherDed, Absences, ot1, amt1, ot2, amt2, ot3, amt3, lateness, amt4, TaxDes, tax, NTaxDes, ntax FROM ModifyVariables WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query54, data1)
                variable_data = cursor.fetchall()
                length = len(variable_data)

                query55 = "SELECT Workingdays FROM employee WHERE EmployeeID = %s"
                cursor.execute(query55,data2)
                wdays = cursor.fetchall()
                for i in range(len(wdays)):
                    wdays = ''.join(wdays[i])

                query56 = "SELECT paysheet_gross From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query56, data1)
                pay_gross = cursor.fetchall()
                for i in range(len(pay_gross)):
                    pay_gross = ''.join(pay_gross[i])

                query57 = "SELECT months FROM employee WHERE EmployeeID = %s"
                cursor.execute(query57,data2)
                months = cursor.fetchall()
                for i in range(len(months)):
                    months = ''.join(months[i])

                return render_template("salary.html", basic=basic, falw=falw, otherded=otherded, ot=ot, disc=disc, nsf=nsf, oalw=oalw, tax=tax, med=med, tran=tran, ntax=ntax, edf=edf, arr=arr, att=att, eoy=eoy, loan=loan, car=car, leave=leave, slevy=slevy, spebns=spebns, late=late, edurel=edurel, speprobns=speprobns, nps=nps, medrel=medrel, payable=payable, ded=ded, net=net, cgross=cgross, pgross=pgross, iet=iet, netch=netch, cpaye=cpaye, ppaye=ppaye, paye=paye, ecsg=ecsg, ensf=ensf, elevy=elevy, absence=absence, eid=eid, fname=fname, lname=lname, pos=pos, month=month, year=year, pnet=pnet, piet=piet, pthes=pthes, ths=ths, plevy=plevy, slevypay = slevypay, netchar=netchar, prgf = prgf, gtax=gtax, vdata = variable_data, length = length, wdays=wdays, paygross = pay_gross, months = months)
# ============================================================================================================================================================================================                
            else:
# ============================================================================================================================================================================================                                
                query1 = "SELECT BasicSalary From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query1, data1)
                basic = cursor.fetchall()
                for i in range(len(basic)):
                    basic = ''.join(basic[i])

                query2 = "SELECT Fixedallow From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query2, data1)
                falw = cursor.fetchall()
                for i in range(len(falw)):
                    falw = ''.join(falw[i])

                query3 = "SELECT OtherDeduction From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query3, data1)
                otherded = cursor.fetchall()
                for i in range(len(otherded)):
                    otherded = ''.join(otherded[i])

                query4 = "SELECT Overtime From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query4, data1)
                ot = cursor.fetchall()
                for i in range(len(ot)):
                    ot = ''.join(ot[i])

                query5 = "SELECT DiscBonus From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query5, data1)
                disc = cursor.fetchall()
                for i in range(len(disc)):
                    disc = ''.join(disc[i])

                query6 = "SELECT NSFEmpee From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query6, data1)
                nsf = cursor.fetchall()
                for i in range(len(nsf)):
                    nsf = ''.join(nsf[i])

                query7 = "SELECT OtherAllow From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query7, data1)
                oalw = cursor.fetchall()
                for i in range(len(oalw)):
                    oalw = ''.join(oalw[i])

                query8 = "SELECT TaxableAllow From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query8, data1)
                tax = cursor.fetchall()
                for i in range(len(tax)):
                    tax = ''.join(tax[i])

                query9 = "SELECT Medical From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query9, data1)
                med = cursor.fetchall()
                for i in range(len(med)):
                    med = ''.join(med[i])

                query10 = "SELECT Transport From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query10, data1)
                tran = cursor.fetchall()
                for i in range(len(tran)):
                    tran = ''.join(tran[i])

                query11 = "SELECT NTaxableAllow From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query11, data1)
                ntax = cursor.fetchall()
                for i in range(len(ntax)):
                    ntax = ''.join(ntax[i])

                query12 = "SELECT EDF From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query12, data1)
                edf = cursor.fetchall()
                for i in range(len(edf)):
                    edf = ''.join(edf[i])

                query13 = "SELECT Arrears From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query13, data1)
                arr = cursor.fetchall()
                for i in range(len(arr)):
                    arr = ''.join(arr[i])

                query14 = "SELECT AttendanceBns From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query14, data1)
                att = cursor.fetchall()
                for i in range(len(att)):
                    att = ''.join(att[i])

                # query15 = "SELECT TravelAllow From OriginalData WHERE EmployeeID = %s AND Month = %s"
                # cursor.execute(query15, data1)
                # travel = cursor.fetchall()
                # for i in range(len(travel)):
                #     travel = ''.join(travel[i])

                query16 = "SELECT EOY From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query16, data1)
                eoy = cursor.fetchall()
                for i in range(len(eoy)):
                    eoy = ''.join(eoy[i])

                query17 = "SELECT Loan From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query17, data1)
                loan = cursor.fetchall()
                for i in range(len(loan)):
                    loan = ''.join(loan[i])

                query18 = "SELECT CarBenefit From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query18, data1)
                car = cursor.fetchall()
                for i in range(len(car)):
                    car = ''.join(car[i])

                query19 = "SELECT LeaveRef From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query19, data1)
                leave = cursor.fetchall()
                for i in range(len(leave)):
                    leave = ''.join(leave[i])

                query20 = "SELECT CurrentSLevy From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query20, data1)
                slevy = cursor.fetchall()
                for i in range(len(slevy)):
                    slevy = ''.join(slevy[i])

                query21 = "SELECT SpecialBns From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query21, data1)
                spebns = cursor.fetchall()
                for i in range(len(spebns)):
                    spebns = ''.join(spebns[i])

                query22 = "SELECT Lateness From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query22, data1)
                late = cursor.fetchall()
                for i in range(len(late)):
                    late = ''.join(late[i])

                query23 = "SELECT EducationRel From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query23, data1)
                edurel = cursor.fetchall()
                for i in range(len(edurel)):
                    edurel = ''.join(edurel[i])

                query24 = "SELECT SpeProBns From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query24, data1)
                speprobns = cursor.fetchall()
                for i in range(len(speprobns)):
                    speprobns = ''.join(speprobns[i])

                query25 = "SELECT NPS From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query25, data1)
                nps = cursor.fetchall()
                for i in range(len(nps)):
                    nps = ''.join(nps[i])

                query26 = "SELECT MedicalRel From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query26, data1)
                medrel = cursor.fetchall()
                for i in range(len(medrel)):
                    medrel = ''.join(medrel[i])

                query27 = "SELECT Payable From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query27, data1)
                payable = cursor.fetchall()
                for i in range(len(payable)):
                    payable = ''.join(payable[i])

                query28 = "SELECT Deduction From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query28, data1)
                ded = cursor.fetchall()
                for i in range(len(ded)):
                    ded = ''.join(ded[i])

                query29 = "SELECT NetPay From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query29, data1)
                net = cursor.fetchall()
                for i in range(len(net)):
                    net = ''.join(net[i])


                query31 = "SELECT CurrentGross From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query31, data1)
                cgross = cursor.fetchall()
                for i in range(len(cgross)):
                    cgross = ''.join(cgross[i])

                query32 = "SELECT PrevGross From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query32, data1)
                pgross = cursor.fetchall()
                for i in range(len(pgross)):
                    pgross = ''.join(pgross[i])

                query33 = "SELECT IET From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query33, data1)
                iet = cursor.fetchall()
                for i in range(len(iet)):
                    iet = ''.join(iet[i])

                query34 = "SELECT NetCh From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query34, data1)
                netch = cursor.fetchall()
                for i in range(len(netch)):
                    netch = ''.join(netch[i])

                query35 = "SELECT CurrentPAYE From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query35, data1)
                cpaye = cursor.fetchall()
                for i in range(len(cpaye)):
                    cpaye = ''.join(cpaye[i])

                query36 = "SELECT PrevPAYE From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query36, data1)
                ppaye = cursor.fetchall()
                for i in range(len(ppaye)):
                    ppaye = ''.join(ppaye[i])

                query37 = "SELECT PAYE From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query37, data1)
                paye = cursor.fetchall()
                for i in range(len(paye)):
                    paye = ''.join(paye[i])

                query38 = "SELECT eCSG From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query38, data1)
                ecsg = cursor.fetchall()
                for i in range(len(ecsg)):
                    ecsg = ''.join(ecsg[i])

                query39 = "SELECT eNSF From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query39, data1)
                ensf = cursor.fetchall()
                for i in range(len(ensf)):
                    ensf = ''.join(ensf[i])

                query40 = "SELECT eLevy From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query40, data1)
                elevy = cursor.fetchall()
                for i in range(len(elevy)):
                    elevy = ''.join(elevy[i])

                query41 = "SELECT Absences From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query41, data1)
                absence = cursor.fetchall()
                for i in range(len(absence)):
                    absence = ''.join(absence[i])

                query42 = "SELECT FirstName From employee WHERE EmployeeID = %s"
                cursor.execute(query42, data2)
                fname = cursor.fetchall()
                for i in range(len(fname)):
                    fname = ''.join(fname[i])

                query43 = "SELECT LastName From employee WHERE EmployeeID = %s"
                cursor.execute(query43, data2)
                lname = cursor.fetchall()
                for i in range(len(lname)):
                    lname = ''.join(lname[i])

                query44 = "SELECT position From employee WHERE EmployeeID = %s"
                cursor.execute(query44, data2)
                pos = cursor.fetchall()
                for i in range(len(pos)):
                    pos = ''.join(pos[i])

                query45 = "SELECT NetPaysheet From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query45, data1)
                pnet = cursor.fetchall()
                for i in range(len(pnet)):
                    pnet = ''.join(pnet[i])            
                
                query46 = "SELECT PrevIET From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query46, data1)
                piet = cursor.fetchall()
                for i in range(len(piet)):
                    piet = ''.join(piet[i])
                
                query47 = "SELECT PrevThreshold From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query47, data1)
                pthes = cursor.fetchall()
                for i in range(len(pthes)):
                    pthes = ''.join(pthes[i])

                query48 = "SELECT Threshold From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query48, data1)
                ths = cursor.fetchall()
                for i in range(len(ths)):
                    ths = ''.join(ths[i])

                query49 = "SELECT PrevSLevy From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query49, data1)
                plevy = cursor.fetchall()
                for i in range(len(plevy)):
                    plevy = ''.join(plevy[i])

                query50 = "SELECT slevyPay From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query50, data1)
                slevypay = cursor.fetchall()
                for i in range(len(slevypay)):
                    slevypay = ''.join(slevypay[i])

                query51 = "SELECT netchar From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query51, data1)
                netchar = cursor.fetchall()
                for i in range(len(netchar)):
                    netchar = ''.join(netchar[i])
                
                query52 = "SELECT PRGF From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query52, data1)
                prgf = cursor.fetchall()
                for i in range(len(prgf)):
                    prgf = ''.join(prgf[i])

                query53 = "SELECT cGrossTax From salary WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query53, data1)
                gtax = cursor.fetchall()
                for i in range(len(gtax)):
                    gtax = ''.join(gtax[i])
                
                print("Before Query Execute")
                query54 = "SELECT Arrears, LocalRef, FixedAllowance, DiscBns, AttBns, Transport, SickRef, SpeBns, OtherAlw, Overseas, OtherDed, Absences, ot1, amt1, ot2, amt2, ot3, amt3, lateness, amt4, TaxDes, tax, NTaxDes, ntax FROM ModifyVariables WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query54, data1)
                variable_data = cursor.fetchall()
                length = len(variable_data)

                query55 = "SELECT Workingdays FROM employee WHERE EmployeeID = %s"
                cursor.execute(query55,data2)
                wdays = cursor.fetchall()
                for i in range(len(wdays)):
                    wdays = ''.join(wdays[i])

                query56 = "SELECT paysheet_gross From OriginalData WHERE EmployeeID = %s AND Month = %s"
                cursor.execute(query56, data1)
                pay_gross = cursor.fetchall()
                for i in range(len(pay_gross)):
                    pay_gross = ''.join(pay_gross[i])

                print("Before Salary 2")

                return render_template("salary2.html", basic=basic, falw=falw, otherded=otherded, ot=ot, disc=disc, nsf=nsf, oalw=oalw, tax=tax, med=med, tran=tran, ntax=ntax, edf=edf, arr=arr, att=att, eoy=eoy, loan=loan, car=car, leave=leave, slevy=slevy, spebns=spebns, late=late, edurel=edurel, speprobns=speprobns, nps=nps, medrel=medrel, payable=payable, ded=ded, net=net, cgross=cgross, pgross=pgross, iet=iet, netch=netch, cpaye=cpaye, ppaye=ppaye, paye=paye, ecsg=ecsg, ensf=ensf, elevy=elevy, absence=absence, eid=eid, fname=fname, lname=lname, pos=pos, month=month, year=year, pnet=pnet, piet=piet, pthes=pthes, ths=ths, plevy=plevy, slevypay = slevypay, netchar=netchar, prgf = prgf, gtax=gtax, vdata = variable_data, length = length, wdays=wdays, paygros = pay_gross)
            # return render_template("salary.html", sal=salary, bonus=bns, car=cars, edf=edf, med = med, travel = talw, eid = eid, fname=first, lname = last, edu=edu, paye=paye, gross=gross, IET=IET, mrel=mrel)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")   
# ===================================================================================================================
    # Save To Database
    elif request.method == "POST" and request.form['action'] == 'save':
        
        print("IN SAVE")

        # Data Of Manually Input Values
        arrears1 = request.form["arr"]
        if arrears1 == "":
            arrears1 = 0
        else:
            arrears1 = arrears1
        
        localRef = request.form["lref"]
        if localRef == "":
            localRef = 0
        else:
            localRef = localRef

        fixedAlw1 = request.form["falw"]
        if fixedAlw1 == "":
            fixedAlw1 = 0
        else:
            fixedAlw1 = fixedAlw1

        discBns1 = request.form["dbns"]
        if discBns1 == "":
            discBns1 = 0
        else:
            discBns1 = discBns1

        attendance1 = request.form["atbns"]
        if attendance1 == "":
            attendance1 = 0
        else:
            attendance1 = attendance1

        transport1 = request.form["tran"]
        if transport1 == "":
            transport1 = 0
        else:
            transport1 = transport1

        sickRef = request.form["sref"]
        if sickRef == "":
            sickRef = 0
        else:
            sickRef = sickRef

        speBns1 = request.form["sbns"]
        if speBns1 == "":
            speBns1 = 0
        else:
            speBns1 = speBns1

        otherAlw1 = request.form["oalw"]
        if otherAlw1 == "":
            otherAlw1 = 0
        else:
            otherAlw1 = otherAlw1

        overseas1 = request.form["oseas"]
        if overseas1 == "":
            overseas1 = 0
        else:
            overseas1 = overseas1

        otherDed1 = request.form["oded"]
        if otherDed1 == "":
            otherDed1 = 0
        else:
            otherDed1 = otherDed1

        absence1 = request.form["abs"]
        if absence1 == "":
            absence1 = 0
        else:
            absence1 = absence1

        ot1 = request.form["hr1"]
        if ot1 == "":
            ot1 = 0
        else:
            ot1 = ot1

        amt1 = request.form["am1"]
        if amt1 == "":
            amt1 = 0
        else:
            amt1 = amt1
        
        ot2 = request.form["hr2"]
        if ot2 == "":
            ot2 = 0
        else:
            ot2 = ot2
        
        amt2 = request.form["am2"]
        if amt2 == "":
            amt2 = 0
        else:
            amt2 = amt2

        ot3 = request.form["hr3"]
        if ot3 == "":
            ot3 = 0
        else:
            ot3 = ot3

        amt3 = request.form["am3"]
        if amt3 == "":
            amt3 = 0
        else:
            amt3 = amt3

        lateness = request.form["hr4"]
        if lateness == "":
            lateness = 0
        else:
            lateness = lateness

        amt4 = request.form["am4"]
        if amt4 == "":
            amt4 = 0
        else:
            amt4 = amt4

        absence_hr = request.form["hr5"]
        if absence_hr == "":
            absence_hr = 0
        else:
            absence_hr = absence_hr

        absence = request.form["abs"]
        if absence == "":
            absence = 0
        else:
            absence = absence

        taxDes = request.form["txdes"]
        if taxDes == "":
            taxDes = " "
        else:
            taxDes = taxDes

        taxamt = request.form["amt1"]
        if taxamt == "":
            taxamt = 0
        else:
            taxamt = taxamt        
        
        ntaxDes = request.form["ntxdes"]
        if ntaxDes == "":
            ntaxDes = " "
        else:
            ntaxDes = ntaxDes
        
        ntaxamt = request.form["amt2"]
        if ntaxamt == "":
            ntaxamt = 0
        else:
            ntaxamt = ntaxamt

        fixedAlw = request.form["falw2"]
        if fixedAlw == "":
            fixedAlw = 0

        otherDed = request.form["oded2"]
        if otherDed == "":
            otherDed = 0

        overtime = request.form["ot2"]
        if overtime == "":
            overtime = 0

        discBns = request.form["dbns2"]
        if discBns == "":
            discBns = 0

        NSF = request.form["nsf"]
        if NSF == "":
            NSF = 0

        otherAlw = request.form["oalw2"]
        if otherAlw == "":
            otherAlw = 0

        tax = request.form["txdes2"]
        if tax == "":
            tax = 0

        medical = request.form["med2"]
        if medical == "":
            medical = 0

        transport = request.form["tran2"]
        if transport == "":
            transport = 0

        ntax = request.form["ntxdes2"]
        if ntax == "":
            ntax = 0

        edf = request.form["edf"]
        if edf == "":
            edf = 0

        arrears = request.form["arr2"]
        if arrears == "":
            arrears = 0

        attendance = request.form["atbns2"]
        if attendance == "":
            attendance = 0

        eoy = request.form["eoy"]
        if eoy == "":
            eoy = 0

        loan = request.form["lrep"]
        if loan == "":
            loan = 0

        car = request.form["car"]
        if car == "":
            car = 0

        leaveRef = request.form["lref2"]
        if leaveRef == "":
            leaveRef = 0

        paye = request.form["paye3"]
        if paye == "":
            paye = 0

        slevy = request.form["levy"]
        if slevy == "":
            slevy = 0

        speBns = request.form["spbonus2"]
        if speBns == "":
            speBns = 0

        lateness = request.form["late"]
        if lateness == "":
            lateness = 0

        educationRel = request.form["edu"]
        if educationRel == "":
            educationRel = 0

        SpeProBns = request.form["spbonus3"]
        if SpeProBns == "":
            SpeProBns = 0

        NPS = request.form["nps"]
        if NPS == "":
            NPS = 0

        medicalRel = request.form["mrel"]
        if medicalRel == "":
            medicalRel = 0

        Payable = request.form["pay"]
        if Payable == "":
            Payable = 0

        Deduction = request.form["ded"]
        if Deduction == "":
            Deduction = 0

        Net = request.form["npay"]
        if Net == "":
            Net = 0

        cgross = request.form["cgrs2"]
        if cgross == "":
            cgross = 0

        pgross = request.form["pgrs"]
        if pgross == "":
            pgross = 0

        iet = request.form["iet"]
        if iet == "":
            iet = 0

        netch = request.form["netch"]
        if netch == "":
            netch = 0

        cpaye = request.form["paye2"]
        if cpaye == "":
            cpaye = 0

        ppaye = request.form["ppaye"]
        if ppaye == "":
            ppaye = 0

        ecsg = request.form["nps2"]
        if ecsg == "":
            ecsg = 0

        ensf = request.form["nsf2"]
        if ensf == "":
            ensf = 0

        elevy = request.form["ivbt"]
        if elevy == "":
            elevy = 0

        prgf = request.form["prgf"]
        if prgf == "":
            prgf = 0

        pthes = request.form["ths2"]
        if pthes == "":
            pthes = 0

        thes = request.form["ths"]
        if thes == "":
            thes = 0

        netchar = request.form["netchar"]
        if netchar == "":
            netchar = 0

        clevy = request.form["clevy"]
        if clevy == "":
            clevy = 0

        plevy = request.form["plevy"]
        if plevy == "":
            plevy = 0

        slevypay = request.form["levypay"]
        if slevypay == "":
            slevypay = 0

        cgtax = request.form["gtax3"]
        if cgtax == "":
            cgtax = 0

        month = request.form["mon"]

        fname = request.form["fname"]

        eid = request.form["eid"]

        UNQ = month + " " + fname

        paysheet_gross = request.form["cgrs"]
        if paysheet_gross == "":
            paysheet_gross = 0

        NetPaysheet = request.form["pnet"]
        if NetPaysheet == "":
            NetPaysheet = 0

        overseas = request.form["oseas"]
        if overseas == "":
            overseas = 0

        otherAlw2 = int(otherAlw) 

        ded = int(Deduction) + int(slevy)
        netpay = int(Payable) - int(ded)
        bonus = int(otherAlw2) + int(fixedAlw) + int(discBns) + int(attendance) + int(overseas)
        NetPaysheet = netpay
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)
            print("Before Query Execute")
            month = request.form["mon"]
            fname = request.form["fname"]

            UNQ = month + " " + fname
            data3 = [UNQ]
            
            query1 = "SELECT salary From employee WHERE EmployeeID = %s"
            cursor.execute(query1, data1)
            basic = cursor.fetchall()
            for i in range(len(basic)):
                basic = ''.join(basic[i])

            query11 = "SELECT LockSal From salary WHERE UNQ = %s"
            cursor.execute(query11,data3)
            lockSal = cursor.fetchall()

            print(lockSal)
            print(len(lockSal))

            if len(lockSal) > 0:
                print("In If")
                for i in range(len(lockSal)):
                    print("In For ")
                    lockSal = ''.join(lockSal[i])
            else:
                print("In Else")
                lockSal = "No"

            if lockSal == "No":
                query1 = """UPDATE salary
                            SET 
                            BasicSalary = %s,
                            FixedAllow = %s,
                            OtherDeduction = %s,
                            Overtime = %s,
                            DiscBonus = %s,
                            NSFEmpee = %s,
                            OtherAllow = %s,
                            TaxableAllow = %s,
                            Medical = %s,
                            Transport = %s,
                            overseas = %s,
                            NTaxableAllow = %s,
                            EDF = %s,
                            Arrears = %s,
                            AttendanceBns = %s,
                            EOY = %s,
                            Loan = %s,
                            CarBenefit = %s,
                            LeaveRef = %s,
                            SLevy = %s,
                            SpecialBns = %s,
                            Lateness = %s,
                            EducationRel = %s,
                            SpeProBns = %s,
                            NPS = %s,
                            MedicalRel = %s,
                            Payable = %s,
                            Deduction = %s,
                            NetPay = %s,
                            NetPaysheet = %s,
                            CurrentGross = %s,
                            cGrossTax = %s,
                            PrevGross = %s,
                            IET = %s,
                            NetCh = %s,
                            CurrentPAYE = %s,
                            PrevPAYE = %s,
                            PAYE = %s,
                            eCSG = %s,
                            eNSF = %s,
                            eLevy = %s,
                            PRGF = %s,
                            PrevThreshold = %s,
                            Threshold = %s,
                            netchar = %s,
                            CurrentSLevy = %s,
                            PrevSLevy = %s,
                            slevyPay = %s,
                            Absences = %s
                            WHERE 
                            UNQ = %s;"""
                data1 = [basic ,fixedAlw, otherDed, overtime, discBns, NSF, otherAlw2, tax, medical, transport, overseas, ntax, edf, arrears, attendance, eoy, loan, car, leaveRef, slevy, speBns, lateness, educationRel, SpeProBns, NPS, medicalRel, Payable, Deduction, Net, NetPaysheet, cgross, cgtax, pgross, iet, netch, cpaye, ppaye, paye, ecsg, ensf, elevy, prgf, pthes, thes, netchar, clevy , plevy, slevypay, absence, UNQ ]
                cursor.execute(query1, data1)
                print("Database Updated Successfully")

                
                query2 = """ UPDATE payslip
                SET
                TravelAlw = %s,
                Bonus = %s,
                Gross = %s,
                PAYE = %s,
                NPF = %s,
                NSF = %s,
                SLevy = %s,
                Deduction = %s,
                NetPay = %s,
                Payable = %s,
                NetPayAcc = %s,
                eNPF = %s,
                eNSF = %s,
                eLevy = %s,
                ePRGF = %s
                WHERE
                UNQ = %s;"""
                
                data2 = [transport, bonus, Payable, paye, NPS, NSF, slevy, ded, netpay, netpay, netpay, ecsg, ensf, elevy, prgf, UNQ ]
                cursor.execute(query2, data2)
                print("update salary complete")
                
                query3 = """ UPDATE payecsv
                SET
                Emoluments = %s,
                PAYE = %s,
                SLevy = %s,
                EmolumentsNet = %s
                WHERE
                UNQ = %s;
                """
                emoluments = int(basic) + int(arrears) + int(overseas) + int(otherAlw) + int(car) + int(overtime) + int(eoy) + int(leaveRef) + int(fixedAlw) + int(discBns) + int(SpeProBns) + int(speBns) 
                data3 = [emoluments, paye, slevypay, emoluments, UNQ]
                cursor.execute(query3, data3)
                print("UPDATE PAYE Query Successfully")

                query5 = "SELECT EmployeeID FROM ModifyVariables WHERE UNQ = %s "
                data5 = [UNQ]
                cursor.execute(query5,data5)
                emp_id = cursor.fetchall()
                
                query6 = """UPDATE prgfcsv
                SET
                Basic = %s,
                Allowance = %s,
                Commission = %s,
                TotalRem = %s,
                PRGF = %s
                WHERE
                UNQ = %s
                ;"""

                totalRem = int(basic) + int(bonus)
                data6 = [basic, bonus, 0, totalRem, prgf, UNQ]
                # cursor.execute(query6, data6)


                query7 = """UPDATE cnpcsv
                SET 
                Basic = %s
                WHERE
                UNQ = %s
                """
                data7 = [basic, UNQ]
                # cursor.execute(query7,data7)

                if emp_id == []:
                    insert_query = """INSERT INTO ModifyVariables(
                        EmployeeID,
                        Arrears,
                        LocalRef,
                        FixedAllowance,
                        DiscBns,
                        AttBns,
                        Transport,
                        SickRef,
                        SpeBns,
                        OtherAlw,
                        Overseas,
                        OtherDed,
                        Absences,
                        ot1,
                        amt1,
                        ot2,
                        amt2,
                        ot3,
                        amt3,
                        lateness,
                        amt4,
                        absenceDays,
                        amt5,
                        TaxDes,
                        tax,
                        NTaxDes,
                        ntax,
                        Month,
                        UNQ
                        )
                        VALUES(
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                        );"""
                    data4 = [eid, arrears1, localRef, fixedAlw1, discBns1, attendance1, transport1, sickRef, speBns1, otherAlw1, overseas1, otherDed1, absence1,ot1, amt1, ot2, amt2, ot3, amt3, lateness, amt4, absence_hr, absence, taxDes, taxamt, ntaxDes, ntaxamt, month, UNQ]
                    cursor.execute(insert_query, data4)
                else:
                    update_query = """UPDATE ModifyVariables
                    SET
                    Arrears = %s,
                    LocalRef = %s,
                    FixedAllowance = %s,
                    DiscBns = %s,
                    AttBns = %s,
                    Transport = %s,
                    SickRef = %s,
                    SpeBns = %s,
                    OtherAlw = %s,
                    Overseas = %s,
                    OtherDed = %s,
                    Absences = %s,
                    ot1 = %s,
                    amt1 = %s,
                    ot2 = %s,
                    amt2 = %s,
                    ot3 = %s,
                    amt3 = %s,
                    lateness = %s,
                    amt4 = %s,
                    absenceDays = %s,
                    amt5 = %s,
                    TaxDes = %s,
                    tax = %s,
                    NTaxDes = %s,
                    ntax = %s
                    WHERE
                    UNQ = %s
                    ;"""
                    data4 = [arrears1, localRef, fixedAlw1, discBns1, attendance1, transport1, sickRef, speBns1, otherAlw1, overseas1, otherDed1, absence1, ot1, amt1, ot2, amt2, ot3, amt3, lateness, amt4, absence_hr, absence, taxDes, taxamt, ntaxDes, ntaxamt, UNQ]
                    cursor.execute(update_query, data4)

                msg = "Salary Modified Successfully"
            else:
                msg = "Salary Already Locked"
            return render_template("salary.html", msg=msg)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template("salary.html")

@app.route("/leave", methods=["GET" , "POST", "PUT"])
def leave():
    # global connection
    if request.method == 'POST':
        eid = request.form['eid']
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True) 

            # query1 = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'employee'"
            # cursor.execute(query1)
            # column_name = cursor.fetchall()

            query1 = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'LeaveData' AND ORDINAL_POSITION BETWEEN 3 AND 5;"
            cursor.execute(query1)
            column_name = cursor.fetchall()
            heading_data = []
            data = []
            print(len(column_name))
            for i in range(len(column_name)):
                print("i : " , i)
                # print("j : ", j)
                data = ''.join(column_name[i])
                print("Data :" + data)
                heading_data.append(data)
            
            print(column_name)
            print(heading_data)

            query2 = f"SELECT Date, LeaveType, LeaveDays FROM LeaveData;"
            cursor.execute(query2)
            table_data = cursor.fetchall()

            print(table_data)

            
            print(eid)
            query3 = f"SELECT Localleave, Sickleave FROM employee WHERE EmployeeID = '{eid}'"
            print(query3)
            cursor.execute(query3)
            leaves = cursor.fetchall()
            print(leaves)
            
            # leave_data = []
            # for i in range(len(leaves)):
            #     print("i : " , i)
            #     # print("j : ", j)
            #     data2 = ''.join(leaves[i])
            #     print("Data2 :" + data2)
            #     leave_data.append(data2)
            # print(leave_data[0])
            # print(leaves[0][0])

            query4 = f"SELECT EmployeeID, FirstName, LastName, Position FROM employee WHERE EmployeeID = '{eid}'"
            cursor.execute(query4)
            personal_data = cursor.fetchall()
            print(personal_data)
            print(personal_data[0][0])

            return render_template("leave.html", heading = heading_data, data = table_data, leaves = leaves, eid=eid,personal = personal_data )
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    print("Before")
    return render_template("leave.html")

@app.route("/lock_salary", methods=["GET" , "POST"])
def lock_salary():
    if request.method == "POST":
        mon = request.form["month"]
        year = request.form["year"]
        
        print(mon)
        print(year)
        mon1 = mon.lower()
        print(mon)

        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)
            
            query = """
            UPDATE salary
            SET
            LockSal = %s
            WHERE
            Month = %s;
            """
            data = ['Yes', mon1]

            cursor.execute(query, data)
            print("Update Query Execute Successfully")
            
            msg = "Locked Salary Of " + mon + " - " + year
            return render_template("lock-salary.html", msg=msg)

        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        
    return render_template("lock-salary.html")

@app.route("/process_salary", methods=["GET" , "POST"])
def process_salary():
    # global connection
    if request.method == "POST":
        eid = request.form["eid"]
        month = request.form["mon"]
        year = request.form["year"]
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)
            if eid != "ALL":
                print("In If")
                
                id = 0
                month = month.lower()
                data = [eid]

                cur_date = date.today()
                res = calendar.monthrange(cur_date.year, cur_date.month)
                day = res[1]

                cur_date = str(cur_date)


                # print(month)
                if month == "January" or month=="january":
                    print("In Jan")

                    current_date = "2022-"+"01-"+"31"
                    
                    id = 1
                elif month == "February" or month=="february":
                    print("In Feb")
                    
                    current_date = "2022-"+"02-"+"31"
                    id = 2
                elif month == "March" or month=="march":
                    print("In Mar")
                    
                    current_date = "2022-"+"03-"+"31"
                    id = 3
                elif month == "April" or month=="april":
                    print("In Apr")
                    
                    current_date = "2022-"+"04-"+"31"
                    id = 4
                elif month == "May" or month=="may":
                    print("In May")
                    
                    current_date = "2022-"+"05-"+"31"
                    id = 5
                elif month == "June" or month=="june":
                    print("In Jun")
                    
                    current_date = "2022-"+"06-"+"31"
                    id = 6
                elif month == "July" or month=="july":
                    print("In Jul")
                    
                    current_date = "2022-"+"07-"+"31"
                    id = 7
                elif month == "August" or month=="august":
                    print("In Aug")
                    
                    current_date = "2022-"+"08-"+"31"
                    id = 8
                elif month == "September" or month=="september":
                    print("In Sep")
                    
                    current_date = "2022-"+"09-"+"31"
                    id = 9
                elif month == "October" or month=="october":
                    print("In Oct")
                    
                    current_date = "2022-"+"10-"+"31"
                    id = 10
                elif month == "November" or month=="november":
                    print("In Nov")
                    
                    current_date = "2022-"+"11-"+"31"
                    id = 11
                elif month == "December" or month=="december":
                    print("In Dec")
                    
                    current_date = "2022-"+"12-"+"31"
                    id = 12
                else:  
                    print("In Else")
                    msg = "Enter Month Correctly"
                    return render_template("process.html", msg = msg)
                
                mid = id-1
                if mid == 0:
                    mid = 12
                
                # print(calendar.month_name[id])
                month2 = calendar.month_name[mid]
                month2 = month2.lower()

                query = "SELECT Carbenefit, salary, Fixedallow, Travelallow, EDF, Educationrel, Medicalrel, medicalrel, Specialbonus, months FROM employee WHERE EmployeeID = %s"
                
                cursor.execute(query, data)
                emp_data = cursor.fetchall()

                # print(emp_data)
                # print(emp_data[0][0])
                # print(emp_data[0][1])

                car = int(emp_data[0][0])                
                tbasic = int(emp_data[0][1])
                fixAllow = int(emp_data[0][2])
                trans = int(emp_data[0][3])
                edf = int(emp_data[0][4])
                education = int(emp_data[0][5])
                Medicalrel = int(emp_data[0][6])
                medical = round(int(emp_data[0][7]) / 12)
                # medical = 0
                SpeProBns = int(emp_data[0][8])
                month_count = int(emp_data[0][9])

                # lwork = emp_data2[10]
                # print(lwork)

                data2 = [eid,month2]
                # print(month2)

                query_month = "SELECT MONTH(Lastwork) AS Month FROM employee WHERE EmployeeID= %s"
                cursor.execute(query_month, data)
                emp_month = cursor.fetchall()
                
                last_mon = emp_month[0][0]
                

                query_year = "SELECT YEAR(Lastwork) AS Year FROM employee WHERE EmployeeID= %s"
                cursor.execute(query_year, data)
                emp_year = cursor.fetchall()

                last_year = emp_year[0][0]

                # if mon == 0:
                #     mon = id
                # if check_date == "11" or get_date > check_date :
                    # print("In If")

                    # query4 = "SELECT hire, position, NICno FROM employee WHERE EmployeeID = %s"
                    # cursor.execute(query4,data)
                    
                msg = "Employee Not Working"

                query1 = "SELECT FirstName FROM employee WHERE EmployeeID = %s"
                cursor.execute(query1,data)
                fname = cursor.fetchall()
                for i in range(len(fname)):
                    fname = ''.join(fname[i])

                UNQ = month + " " + fname
                data3 = [UNQ]

                hire_date = "SELECT hire FROM employee WHERE EmployeeID= %s"
                cursor.execute(hire_date, data)
                hire_date_emp = cursor.fetchall()

                hire_dt = str(hire_date_emp[0][0])

                print("Hire Date ", hire_dt)
                print("Current Date " , current_date)

                pension_query = "SELECT NPS FROM employee WHERE EmployeeID= %s"
                cursor.execute(pension_query , data)
                pension = cursor.fetchall()

                pension = pension[0][0]

                expatriate_query = "SELECT expatriate FROM employee WHERE EmployeeID = %s"
                cursor.execute(expatriate_query, data)
                expatriate = cursor.fetchall()

                expatriate = expatriate[0][0]

                if (int(last_year) >= int(year) or (last_year == 1 and last_mon == 1)) and (hire_dt <= cur_date):
                    print("Year Is Correct")
                    if int(last_mon) >= int(id) or (last_year == 1 and last_mon == 1):
                        print("In Start Process")
                        if pension == 'Paid':
                            query2 = "SELECT LastName FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query2,data)
                            lname = cursor.fetchall()
                            for i in range(len(lname)):
                                lname = ''.join(lname[i])

                            query3 = "SELECT cGrossTax FROM salary WHERE EmployeeID= %s AND Month = %s"
                            cursor.execute(query3,data2)
                            prevGross = cursor.fetchall()
                            for i in range(len(prevGross)):
                                if prevGross != None:
                                    prevGross = ''.join(prevGross[i])
                                else:
                                    prevGross = 0
                            if prevGross != 0:
                                prevGross = ''.join(map(str,prevGross))
                                

                            query4 = "SELECT IET FROM salary WHERE EmployeeID= %s AND Month = %s"
                            cursor.execute(query4,data2)
                            piet = cursor.fetchall()
                            for i in range(len(piet)):
                                if piet != None:
                                    piet = ''.join(piet[i])
                                else:
                                    piet = 0
                            if piet != 0:
                                piet = ''.join(map(str,piet))

                            query5 = "SELECT CurrentPAYE FROM salary WHERE EmployeeID= %s AND Month = %s"
                            cursor.execute(query5,data2)
                            ppaye = cursor.fetchall()
                            # print(ppaye)
                            for i in range(len(ppaye)):
                                if ppaye != None:
                                    ppaye = ''.join(ppaye[i])
                                else:
                                    ppaye = 0
                            if ppaye != 0:
                                ppaye = ''.join(map(str,ppaye))

                            query6 = "SELECT Threshold FROM salary WHERE EmployeeID= %s AND Month = %s"
                            cursor.execute(query6,data2)
                            pths = cursor.fetchall()
                            for i in range(len(pths)):
                                if pths != None:
                                    pths = ''.join(pths[i])
                                else:
                                    pths = 0
                            if pths != 0:
                                pths = ''.join(map(str,pths))

                            query7 = "SELECT CurrentSLevy FROM salary WHERE EmployeeID= %s AND Month = %s"
                            cursor.execute(query7,data2)
                            plevy = cursor.fetchall()

                            if len(plevy) > 0:
                                for i in range(len(plevy)):
                                    plevy = ''.join(plevy[i])
                            else:
                                plevy = 0    


                            # for i in range(len(plevy)):
                            #     print("In For")
                            #     if plevy != None:
                            #         print("In if1")
                            #         plevy = ''.join(plevy[i])
                            #     else:
                            #         print("In Else")
                            #         plevy = 0
                            
                            # if plevy != 0:
                            #     print("In if2")
                            #     plevy = ''.join(map(str,plevy))
                            

                            query8 = "SELECT hire FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query8,data)
                            hire = cursor.fetchall()
                            
                            hire = hire[0][0] 
                            hire = str(hire)
                            # print(hire)
                            # print(str(hire))
                            # print(type(str(hire)))
                            # if hire != None:
                            #     for i in range(len(hire)):
                            #         hire = ''.join(hire[i])
                            #     hire = ''.join(map(str,hire))
                            # else:
                            #     hire = 0                    

                            query9 = "SELECT position FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query9,data)
                            pos = cursor.fetchall()
                            for i in range(len(pos)):
                                if pos != None:
                                    pos = ''.join(pos[i])
                                else:
                                    pos = " "
                            if pos != 0:
                                pos = ''.join(map(str,pos))
                            # print(pos)
                            

                            query10 = "SELECT NICno FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query10,data)
                            nic = cursor.fetchall()
                            # print(nic)
                            for i in range(len(nic)):
                                if nic[0][0] != None:
                                    nic = ''.join(nic[i])
                                else:
                                    nic = " "
                            if nic != 0:
                                nic = ''.join(map(str,nic))
                            
                            UNQ = month + " " + fname
                            data3 = [UNQ]
                            
                            # query11 = "SELECT LockSal From salary WHERE UNQ = %s"
                            # cursor.execute(query11,data3)
                            # lockSal = cursor.fetchall()

                            # print(lockSal)
                            # print(len(lockSal))

                            # if len(lockSal) > 0:
                            #     print("In If")
                            #     for i in range(len(lockSal)):
                            #         print("In For ")
                            #         lockSal = ''.join(lockSal[i])
                            # else:
                            #     print("In Else")
                            #     lockSal = "No"

                            # query12 = "SELECT working FROM employee WHERE EmployeeID = %s"
                            # cursor.execute(query12, data)
                            # working = cursor.fetchall()

                            # if len(working) > 0:
                            #     print("In If")
                            #     for i in range(len(working)):
                            #         print("In For ")
                            #         working = ''.join(working[i])
                            # else:
                            #     print("In Else")
                            #     working = "Yes"                
                            
                            flname = lname + " " + fname

                            # Values We Don't Get
                            ot = 0
                            otherAllow = 0
                            arrears = 0
                            eoy = 0
                            leave = 0
                            speBns = 0
                            discBns = 0
                            tax = 0
                            ntax = 0
                            attBns = 0
                            overseas = tax + ntax

                            loan = 0
                            lateness = 0
                            otherDed = 0
                            ab = 0

                            # Previous Data
                            # print(type(prevGross))
                            # print(prevGross)
                            if prevGross == "":
                                prevGross = 0
                            else:
                                prevGross = int(prevGross)

                            if piet == "":
                                piet = 0
                            else:
                                piet = int(piet)
                            
                            if ppaye == "":
                                ppaye = 0
                            else:
                                ppaye = int(ppaye)
                            
                            if pths == "":
                                pths = 0
                            else:
                                pths = int(pths)
                            # print(pths)
                            if plevy == "":
                                plevy = 0
                            else:
                                plevy = int(plevy)
                    
                            basic = int(tbasic) - int(ab)
                            # Calculations
                            payable = basic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns
                            bonus = speBns + SpeProBns + otherAllow + fixAllow + discBns + attBns

                            pay_gross = tbasic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns

                            # For Overseas Amount
                            if overseas > 0:
                                ntax = round(int(basic) * 0.06)
                                tax = round(int(overseas) - int(ntax))
                            else:
                                ntax = 0
                                tax = 0

                            if trans > 20000:
                                transTax = trans - 20000
                                ntransTax = trans - transTax
                            else:
                                transTax = 0
                                ntransTax = 0

                            cgross = basic + ot + otherAllow + trans + arrears + eoy + leave + discBns + fixAllow + tax + SpeProBns + attBns + car

                            grossTax = basic + ot + transTax +otherAllow + arrears + eoy + leave + discBns + fixAllow  + tax + SpeProBns + attBns + car

                            # print("prev Gross " , prevGross)
                            # print("Curr Gross " , cgross)
                            gross = prevGross + grossTax
                            # print("gross" , gross)
                            medf = round(int(edf) / int(month_count))
                            ciet = round(( int(edf) + int(Medicalrel) + int(education)) / int(month_count))
                            
                            iet = int(ciet) + int(piet)
                            # print("ciet" , ciet)
                            # print("piet", piet)
                            # print("iet", iet)

                            netch = gross - iet

                            # print("netch" , netch)
                            if netch < 0:
                                netch = 0
                            else:
                                netch = netch

                            if int(basic) > 50000:
                                nps = round(basic * 0.03)
                                # cpaye =  round(netch * 0.15)
                                enps = round(basic * 0.06)
                            else:
                                nps = round(basic * 0.015)
                                # cpaye = round(netch * 0.1)
                                enps = round(basic * 0.03)

                            check = int(basic) + int(otherAllow) - int(medf)
                            if check < 53846:
                                cpaye = round(netch* 0.1)
                            elif check >= 53846 and check < 75000:
                                cpaye = round(netch* 0.125)
                            else:
                                cpaye = round(netch* 0.15)

                            if cpaye < 0:
                                cpaye = 0
                            else:
                                cpaye = int(cpaye)
                            
                            if ppaye < 0:
                                ppaye =0
                            else:
                                ppaye = int(ppaye)

                            # print("cpaye", cpaye)
                            # print("ppaye", ppaye)
                            paye = int(cpaye) - int(ppaye)
                            # print("paye", paye)
                            if paye < 0:
                                paye =0
                            else:
                                paye = int(paye)

                            nsf = int(basic * 0.01)

                            if nsf > 214:
                                nsf = 214
                            else:
                                nsf = int(nsf)

                            temp = int(cgross) * 13
                            slevy = 0
                            tths = round(3000000/12)
                            ths = int(pths) + int(tths)
                            # print(ths)
                            netchar = int(gross) - int(iet) - int(ths)
                            
                            if netchar < 0 :
                                netchar = 0
                            else:
                                netchar = netchar

                            if int(temp) > 3000000:
                                slevy1 = round(netchar * 0.25)
                                slevy2 = round(gross * 0.1)
                                
                                if slevy1 > slevy2:
                                    slevy = int(slevy2)
                                else:
                                    slevy = int(slevy1)
                            else:
                                slevy = 0
                            
                            ensf = round(basic * 0.025)
                            if ensf > 536:
                                ensf = 536
                            else:
                                ensf = round(ensf)
                            levy = round(int(basic) * 0.015)
                            deduction = int(loan) + int(paye) + int(lateness) + int(nps) + int(otherDed) + int(nsf) + int(medical)
                            net = int(payable) - int(deduction)
                            # print(slevy)
                            
                            slevypay = slevy - plevy
                            NetPaysheet = int(net) - int(slevypay)
                            
                            otherAllow2 = int(otherAllow) 
                            
                            tax = int(tax) + int(transTax)
                            ntax = int(ntax) + int(ntransTax)
                            # Payslip Calculation

                            paygross = int(basic) + int(trans) + int(bonus)

                            totalDeduction = int(paye) + int(nps) + int(nsf) + int(slevypay)

                            netpay = paygross - totalDeduction
                            # eprgf = 0

                            if expatriate == "No":
                                if basic < 200000:
                                    eprgf = round((int(basic) + int(bonus)) * 0.035) # + commission
                                else:
                                    eprgf = 0
                            else:
                                eprgf = 0
                        else:
                            query2 = "SELECT LastName FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query2,data)
                            lname = cursor.fetchall()
                            for i in range(len(lname)):
                                lname = ''.join(lname[i])

                            prevGross = 0                                

                            piet = 0

                            ppaye = 0

                            pths = 0
 
                            plevy = 0    

                            query8 = "SELECT hire FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query8,data)
                            hire = cursor.fetchall()
                            
                            hire = hire[0][0] 
                            hire = str(hire)
                            
                            query9 = "SELECT position FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query9,data)
                            pos = cursor.fetchall()
                            for i in range(len(pos)):
                                if pos != None:
                                    pos = ''.join(pos[i])
                                else:
                                    pos = " "
                            if pos != 0:
                                pos = ''.join(map(str,pos))
                            # print(pos)
                            

                            query10 = "SELECT NICno FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query10,data)
                            nic = cursor.fetchall()
                            # print(nic)
                            for i in range(len(nic)):
                                if nic[0][0] != None:
                                    nic = ''.join(nic[i])
                                else:
                                    nic = " "
                            if nic != 0:
                                nic = ''.join(map(str,nic))
                            
                            UNQ = month + " " + fname
                            data3 = [UNQ]
                            
                            flname = lname + " " + fname

                            # Values We Don't Get
                            ot = 0
                            otherAllow = 0
                            arrears = 0
                            eoy = 0
                            leave = 0
                            speBns = 0
                            discBns = 0
                            tax = 0
                            ntax = 0
                            attBns = 0
                            overseas = tax + ntax

                            loan = 0
                            lateness = 0
                            otherDed = 0
                            ab = 0
                    
                            basic = int(tbasic) - int(ab)
                            # Calculations
                            payable = basic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns
                            bonus = speBns + SpeProBns + otherAllow + fixAllow + discBns + attBns

                            pay_gross = tbasic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns

                            # For Overseas Amount
                            # if overseas > 0:
                            #     ntax = round(int(basic) * 0.06)
                            #     tax = round(int(overseas) - int(ntax))
                            # else:
                            #     ntax = 0
                            #     tax = 0

                            if trans > 20000:
                                transTax = trans - 20000
                                ntransTax = trans - transTax
                            else:
                                transTax = 0
                                ntransTax = trans

                            cgross = basic + ot + otherAllow + trans + arrears + eoy + leave + discBns + fixAllow + tax + SpeProBns + attBns + car

                            grossTax = basic + ot + transTax +otherAllow + arrears + eoy + leave + discBns + fixAllow  + tax + SpeProBns + attBns + car

                            # print("prev Gross " , prevGross)
                            # print("Curr Gross " , cgross)
                            gross = prevGross + grossTax
                            # print("gross" , gross)
                            medf = round(int(edf) / int(month_count))
                            ciet = round(( int(edf) + int(Medicalrel) + int(education)) / int(month_count))
                            
                            iet = int(ciet) + int(piet)
                            # print("ciet" , ciet)
                            # print("piet", piet)
                            # print("iet", iet)

                            netch = gross - iet

                            # print("netch" , netch)
                            if netch < 0:
                                netch = 0
                            else:
                                netch = netch

                            nps = 0
                            enps = 0
                            cpaye = 0
                            ppaye = 0

                            # if int(basic) > 50000:
                            #     nps = round(basic * 0.03)
                            #     # cpaye =  round(netch * 0.15)
                            #     enps = round(basic * 0.06)
                            # else:
                            #     nps = round(basic * 0.015)
                            #     # cpaye = round(netch * 0.1)
                            #     enps = round(basic * 0.03)

                            # check = int(basic) + int(otherAllow) - int(medf)
                            # if check < 53846:
                            #     cpaye = round(netch* 0.1)
                            # elif check >= 53846 and check < 75000:
                            #     cpaye = round(netch* 0.125)
                            # else:
                            #     cpaye = round(netch* 0.15)

                            # if cpaye < 0:
                            #     cpaye = 0
                            # else:
                            #     cpaye = int(cpaye)
                            
                            # if ppaye < 0:
                            #     ppaye =0
                            # else:
                            #     ppaye = int(ppaye)

                            # print("cpaye", cpaye)
                            # print("ppaye", ppaye)
                            # paye = int(cpaye) - int(ppaye)
                            # print("paye", paye)
                            # if paye < 0:
                            #     paye =0
                            # else:
                            #     paye = int(paye)

                            nsf = 0
                            # nsf = int(basic * 0.01)

                            # if nsf > 214:
                            #     nsf = 214
                            # else:
                            #     nsf = int(nsf)

                            temp = int(cgross) * 13
                            slevy = 0
                            tths = round(3000000/int(month_count))
                            ths = int(pths) + int(tths)
                            # print(ths)
                            netchar = int(gross) - int(iet) - int(ths)
                            
                            if netchar < 0 :
                                netchar = 0
                            else:
                                netchar = netchar

                            # if int(temp) > 3000000:
                            #     slevy1 = round(netchar * 0.25)
                            #     slevy2 = round(gross * 0.1)
                                
                            #     if slevy1 > slevy2:
                            #         slevy = int(slevy2)
                            #     else:
                            #         slevy = int(slevy1)
                            # else:
                            #     slevy = 0

                            slevy = 0

                            ensf = 0
                            
                            # ensf = round(basic * 0.025)
                            # if ensf > 536:
                            #     ensf = 536
                            # else:
                            #     ensf = round(ensf)

                            levy = 0
                            # levy = round(int(basic) * 0.015)
                            deduction = int(loan) + int(paye) + int(lateness) + int(nps) + int(otherDed) + int(nsf) + int(medical)
                            net = int(payable) - int(deduction)
                            # print(slevy)
                            
                            slevypay = slevy - plevy
                            NetPaysheet = int(net) - int(slevypay)
                            
                            otherAllow2 = int(otherAllow) 
                            
                            tax = int(tax) + int(transTax)
                            ntax = int(ntax) + int(ntransTax)
                            # Payslip Calculation

                            paygross = int(basic) + int(trans) + int(bonus)

                            totalDeduction = int(paye) + int(nps) + int(nsf) + int(slevypay)

                            netpay = paygross - totalDeduction
                            # eprgf = 0
                            if expatriate == "No":
                                if basic < 200000:
                                    eprgf = round((int(basic) + int(bonus)) * 0.035) # + commission
                                else:
                                    eprgf = 0
                            else:
                                eprgf = 0

                        get_original  = "SELECT EmployeeID FROM OriginalData WHERE UNQ = %s"
                        cursor.execute(get_original, data3)
                        original_id = cursor.fetchall()

                        if original_id == []:
                            insert_query = """
                                INSERT INTO OriginalData(
                                EmployeeID,
                                EmployeeName,
                                BasicSalary,
                                FixedAllow,
                                OtherDeduction,
                                Overtime,
                                DiscBonus,
                                NSFEmpee,
                                OtherAllow,
                                TaxableAllow,
                                Medical,
                                Transport,
                                overseas,
                                NTaxableAllow,
                                EDF,
                                Arrears,
                                AttendanceBns,
                                EOY,
                                Loan,
                                CarBenefit,
                                LeaveRef,
                                SLevy,
                                SpecialBns,
                                Lateness,
                                EducationRel,                    
                                SpeProBns,
                                NPS,
                                MedicalRel,
                                Payable,
                                Deduction,
                                NetPay,
                                NetPaysheet,
                                paysheet_gross,
                                CurrentGross,
                                cGrossTax,
                                PrevGross,
                                PrevIET,
                                IET,
                                NetCh,
                                CurrentPAYE,
                                PrevPAYE,
                                PAYE,
                                eCSG,
                                eNSF,
                                eLevy,
                                PRGF,
                                PrevThreshold,
                                Threshold,
                                netchar,
                                CurrentSLevy,
                                PrevSLevy,
                                slevyPay,
                                Absences,
                                Month,
                                Year,
                                UNQ,
                                LockSal
                                )

                                VALUES(
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                                );
                                """
                            data_original = [eid, flname, basic , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoy, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, pay_gross, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, month, year, UNQ, 'No']
                            cursor.execute(insert_query, data_original)
                            print("Original Data Insert Query Executed")
                        else:
                            update_original = """UPDATE OriginalData
                                            SET
                                            EmployeeID = %s,
                                            EmployeeName = %s,
                                            BasicSalary = %s,
                                            FixedAllow = %s,
                                            OtherDeduction = %s,
                                            Overtime = %s,
                                            DiscBonus = %s,
                                            NSFEmpee = %s,
                                            OtherAllow = %s,
                                            TaxableAllow = %s,
                                            Medical = %s,
                                            Transport = %s,
                                            overseas = %s,
                                            NTaxableAllow = %s,
                                            EDF = %s,
                                            Arrears = %s,
                                            AttendanceBns = %s,
                                            EOY = %s,
                                            Loan = %s,
                                            CarBenefit = %s,
                                            LeaveRef = %s,
                                            SLevy = %s,
                                            SpecialBns = %s,
                                            Lateness = %s,
                                            EducationRel = %s,
                                            SpeProBns = %s,
                                            NPS = %s,
                                            MedicalRel = %s,
                                            Payable = %s,
                                            Deduction = %s,
                                            NetPay = %s,
                                            NetPaysheet = %s,
                                            paysheet_gross = %s,
                                            CurrentGross = %s,
                                            cGrossTax = %s,
                                            PrevGross = %s,
                                            PrevIET = %s,
                                            IET = %s,
                                            NetCh = %s,
                                            CurrentPAYE = %s,
                                            PrevPAYE = %s,
                                            PAYE = %s,
                                            eCSG = %s,
                                            eNSF = %s,
                                            eLevy = %s,
                                            PRGF = %s,
                                            PrevThreshold = %s,
                                            Threshold = %s,
                                            netchar = %s,
                                            CurrentSLevy = %s,
                                            PrevSLevy = %s,
                                            slevyPay = %s,
                                            Absences = %s
                                            WHERE 
                                            UNQ = %s;
                                            """
                            data_original = [eid, flname, basic , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoy, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, pay_gross, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, UNQ]
                            cursor.execute(update_original, data_original)
                            print("Update Original Query Executed")

                        get_salary  = "SELECT EmployeeID FROM salary WHERE UNQ = %s"
                        cursor.execute(get_salary, data3)
                        salary_id = cursor.fetchall()

                        if salary_id == []:
                            insert_query2 = """
                                INSERT INTO salary(
                                EmployeeID,
                                EmployeeName,
                                BasicSalary,
                                FixedAllow,
                                OtherDeduction,
                                Overtime,
                                DiscBonus,
                                NSFEmpee,
                                OtherAllow,
                                TaxableAllow,
                                Medical,
                                Transport,
                                overseas,
                                NTaxableAllow,
                                EDF,
                                Arrears,
                                AttendanceBns,
                                EOY,
                                Loan,
                                CarBenefit,
                                LeaveRef,
                                SLevy,
                                SpecialBns,
                                Lateness,
                                EducationRel,                    
                                SpeProBns,
                                NPS,
                                MedicalRel,
                                Payable,
                                Deduction,
                                NetPay,
                                NetPaysheet,
                                paysheet_gross,
                                CurrentGross,
                                cGrossTax,
                                PrevGross,
                                PrevIET,
                                IET,
                                NetCh,
                                CurrentPAYE,
                                PrevPAYE,
                                PAYE,
                                eCSG,
                                eNSF,
                                eLevy,
                                PRGF,
                                PrevThreshold,
                                Threshold,
                                netchar,
                                CurrentSLevy,
                                PrevSLevy,
                                slevyPay,
                                Absences,
                                Month,
                                Year,
                                UNQ,
                                LockSal,
                                ProcSal
                                )

                                VALUES(
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                                );
                                """
                            data_salary = [eid, flname, basic , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoy, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, pay_gross, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, month, year, UNQ, 'No', 'Yes']
                            cursor.execute(insert_query2, data_salary)
                            print("Salary Insert Query Executed")
                        else:
                            update_salary = """UPDATE salary
                                            SET
                                            EmployeeID = %s,
                                            EmployeeName = %s,
                                            BasicSalary = %s,
                                            FixedAllow = %s,
                                            OtherDeduction = %s,
                                            Overtime = %s,
                                            DiscBonus = %s,
                                            NSFEmpee = %s,
                                            OtherAllow = %s,
                                            TaxableAllow = %s,
                                            Medical = %s,
                                            Transport = %s,
                                            overseas = %s,
                                            NTaxableAllow = %s,
                                            EDF = %s,
                                            Arrears = %s,
                                            AttendanceBns = %s,
                                            EOY = %s,
                                            Loan = %s,
                                            CarBenefit = %s,
                                            LeaveRef = %s,
                                            SLevy = %s,
                                            SpecialBns = %s,
                                            Lateness = %s,
                                            EducationRel = %s,
                                            SpeProBns = %s,
                                            NPS = %s,
                                            MedicalRel = %s,
                                            Payable = %s,
                                            Deduction = %s,
                                            NetPay = %s,
                                            NetPaysheet = %s,
                                            paysheet_gross = %s,
                                            CurrentGross = %s,
                                            cGrossTax = %s,
                                            PrevGross = %s,
                                            PrevIET = %s,
                                            IET = %s,
                                            NetCh = %s,
                                            CurrentPAYE = %s,
                                            PrevPAYE = %s,
                                            PAYE = %s,
                                            eCSG = %s,
                                            eNSF = %s,
                                            eLevy = %s,
                                            PRGF = %s,
                                            PrevThreshold = %s,
                                            Threshold = %s,
                                            netchar = %s,
                                            CurrentSLevy = %s,
                                            PrevSLevy = %s,
                                            slevyPay = %s,
                                            Absences = %s
                                            WHERE
                                            UNQ = %s
                                            """
                            
                            data_salary = [eid, flname, basic , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoy, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, pay_gross, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, UNQ]
                            cursor.execute(update_salary, data_salary)
                            print("Update Salary Query Executed")

                        get_payslip  = "SELECT EmpName FROM payslip WHERE UNQ = %s"
                        cursor.execute(get_payslip, data3)
                        payslip_id = cursor.fetchall()

                        if payslip_id == []:
                            query = """INSERT INTO payslip(
                                        JoinDate,
                                        Company,
                                        EmpName,
                                        Position,
                                        NIC,
                                        BasicSalary,
                                        TravelAlw,
                                        Bonus,
                                        Gross,
                                        PAYE,
                                        NPF,
                                        NSF,
                                        SLevy,
                                        Deduction,
                                        NetPay,
                                        Payable,
                                        NetPayAcc,
                                        eNPF,
                                        eNSF,
                                        eLevy,
                                        ePRGF,
                                        month,
                                        year,
                                        UNQ
                                        )
                                        VALUES(
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s
                                        );
                                        """
                                
                            data_payslip = [hire, "CARE Ratings (Africa) Private Limitedivate Limited" , flname, pos, nic, basic, trans, bonus, paygross, paye, nps, nsf, slevypay , totalDeduction, netpay,netpay, netpay, enps, ensf, levy, eprgf, month, year, UNQ ]
                            cursor.execute(query, data_payslip)
                            print("Payslip Insert Query Executed")
                        else:
                            update_payslip = """UPDATE payslip
                                    SET
                                    EmpName = %s,
                                    Position = %s,
                                    NIC = %s,
                                    BasicSalary = %s,
                                    TravelAlw = %s,
                                    Bonus = %s,
                                    Gross = %s,
                                    PAYE = %s,
                                    NPF = %s,
                                    NSF = %s,
                                    SLevy = %s,
                                    Deduction = %s,
                                    NetPay = %s,
                                    Payable = %s,
                                    NetPayAcc = %s,
                                    eNPF = %s,
                                    eNSF = %s,
                                    eLevy = %s,
                                    ePRGF = %s,
                                    month = %s
                                    WHERE
                                    UNQ = %s;
                                    """
                            data_payslip = [flname, pos, nic, basic, trans, bonus, paygross, paye, nps, nsf, slevypay, totalDeduction, netpay, netpay, netpay,  enps, ensf, levy, eprgf, month, UNQ]
                            cursor.execute(update_payslip, data_payslip)
                            print("Update Payslip Query Executed")
                        # msg = "Processing Complete"

                        print("Before NIC Query")
                        query14 = "SELECT NICno FROM employee WHERE EmployeeID = %s"
                        cursor.execute(query14, data)
                        nic = cursor.fetchall()
                        if nic[0][0] == "":
                            nic = " "
                        else:
                            for i in range(len(nic)):
                                nic = ''.join(nic[i])

                        emolument = int(basic) + int(arrears) + int(overseas) + int(otherAllow) + int(car) + int(ot) + int(eoy) + int(leave) + int(fixAllow) + int(discBns) + int(SpeProBns) + int(speBns) 

                        print("Before Paye Query")
                        get_payecsv  = "SELECT EmployeeID FROM payecsv WHERE UNQ = %s"
                        cursor.execute(get_payecsv, data3)
                        payecsv_id = cursor.fetchall()

                        print("Before NPS Query")
                        query12 = "SELECT NPS FROM employee WHERE EmployeeID = %s"
                        cursor.execute(query12, data)
                        pension = cursor.fetchall()
                        for i in range(len(pension)):
                            pension = ''.join(pension[i])

                        if pension == "Paid":
                            pension = "Yes"
                        else:
                            pension = "No"

                        print("Before working query")
                        query13 = "SELECT working FROM employee WHERE EmployeeID = %s"
                        cursor.execute(query13, data)
                        working = cursor.fetchall()
                        for i in range(len(working)):
                            working = ''.join(working[i])

                        allowance = int(otherAllow) + int(fixAllow) + int(speBns) + int(SpeProBns) + int(discBns) + int(attBns)
                        commission = 0

                        totalRem = int(basic) + int(allowance)

                        print("Before PRGF Query")
                        get_prgfcsv  = "SELECT EmployeeID FROM prgfcsv WHERE UNQ = %s"
                        cursor.execute(get_prgfcsv, data3)
                        prgfcsv_id = cursor.fetchall()

                        if expatriate == "No":
                            print("In Expatriate")
                            if payecsv_id == []:
                                print("In If Payecsv")
                                paye_query = """ INSERT INTO payecsv(
                                                EmployeeID,
                                                LastName,
                                                FirstName,
                                                Emoluments,
                                                PAYE,
                                                working,
                                                SLevy,
                                                EmolumentsNet,
                                                month,
                                                UNQ
                                                )
                                                VALUES(
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s
                                                );"""
                                data_paye = [nic, lname, fname, emolument, paye, 'Yes', slevypay, emolument, month, UNQ]

                                cursor.execute(paye_query, data_paye)
                                print("PAYE Query Executed")
                            else:
                                print("In else Payecsv")
                                update_payecsv = """UPDATE payecsv
                                                SET
                                                EmployeeID = %s,
                                                LastName = %s,
                                                FirstName = %s,
                                                Emoluments = %s,
                                                PAYE = %s,
                                                SLevy = %s,
                                                EmolumentsNet = %s
                                                WHERE
                                                UNQ = %s;
                                                """

                                data_paye = [nic, lname, fname, emolument, paye, slevypay, emolument, UNQ]
                                cursor.execute(update_payecsv, data_paye)
                                print("Update PAYE CSV Query Executed")

                            if prgfcsv_id == []:
                                prgf_query = """INSERT INTO prgfcsv(
                                                EmployeeID,
                                                LastName,
                                                FirstName,
                                                Pension,
                                                Working,
                                                Hire,
                                                Basic,
                                                Allowance,
                                                Commission,
                                                TotalRem,
                                                PRGF,
                                                reason,
                                                month,
                                                UNQ
                                                )
                                                VALUES(
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s
                                                );"""
                                if basic < 200000:
                                    data_prgf = [nic, lname, fname, "No", working, hire, basic, allowance, commission, totalRem, eprgf, " " , month, UNQ]
                                else:
                                    data_prgf = [nic, lname, fname, "No", working, hire, basic, 0, 0, 0, 0, " " , month, UNQ]
                                
                                cursor.execute(prgf_query, data_prgf)
                                print("PRGF Insert Query Executed")
                            
                            else:
                                update_prgf = """UPDATE prgfcsv
                                            SET
                                            EmployeeID = %s,
                                            LastName = %s,
                                            FirstName = %s,
                                            Basic = %s,
                                            Allowance = %s,
                                            Commission = %s,
                                            TotalRem = %s,
                                            PRGF = %s
                                            WHERE
                                            UNQ = %s;
                                            """
                                prgf_data = [eid, lname, fname, basic, allowance, commission, totalRem, eprgf, UNQ]

                                cursor.execute(update_prgf, prgf_data)
                                print("Update PRGF Complete")

                            get_cnpcsv  = "SELECT EmployeeID FROM prgfcsv WHERE UNQ = %s"
                            cursor.execute(get_cnpcsv, data3)
                            cnpcsv_id = cursor.fetchall()

                            if cnpcsv_id == []:
                                cnp_query = """INSERT INTO cnpcsv(
                                            EmployeeID,
                                            LastName,
                                            FirstName,
                                            Basic,
                                            Basic2,
                                            Season,
                                            Alphabet,
                                            Number,
                                            Working,
                                            Blank1,
                                            Blank2,
                                            month,
                                            UNQ
                                            )
                                            VALUES(
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s
                                            );"""
                                data_cnp = [nic, lname, fname, basic, basic, "S2", "M", "1", working, " ", " ", month, UNQ]

                                cursor.execute(cnp_query, data_cnp)
                                print("CNP Insert Query Executed")

                            else:
                                update_cnp = """UPDATE cnpcsv
                                            SET
                                            EmployeeID = %s,
                                            LastName = %s,
                                            FirstName = %s,
                                            Basic = %s,
                                            Basic2 = %s
                                            WHERE
                                            UNQ = %s;
                                            """
                                cnp_data = [eid, lname, fname, basic, basic, UNQ]
                                cursor.execute(update_cnp, cnp_data)

                                print("Update CNP Complete")

                        print("Before contribution query")
                        get_contribution  = "SELECT EmployeeID FROM contribution WHERE UNQ = %s"
                        print("Before Cursor")
                        print("data3 ", data3)
                        cursor.execute(get_contribution, data3)
                        print("After Cursor")
                        contri_id = cursor.fetchall()
                        print("After Fetchall")

                        print(contri_id)

                        if contri_id == []:
                            print("In Contri If")
                            insert_contri = """INSERT INTO contribution(
                                                EmployeeID,
                                                LastName,
                                                FirstName,
                                                IDCard,
                                                Salary,
                                                blank1,
                                                ecsg,
                                                elevy,
                                                ensf,
                                                prgf,
                                                csg,
                                                nsf,
                                                slevy,
                                                paye,
                                                month,
                                                year,
                                                UNQ
                                                )
                                                VALUES(
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s
                                                );
                                                """
                            contri_data = [eid, lname, fname, nic, basic, " ", enps, levy, ensf, eprgf, nps, nsf, slevypay, paye,  month, year, UNQ]
                            cursor.execute(insert_contri, contri_data)
                            print("Contribution Insert Query Executed")

                        else:
                            print("IN Contri Else")
                            update_contri = """UPDATE contribution
                                            SET
                                            EmployeeID = %s,
                                            LastName = %s,
                                            FirstName = %s,
                                            Salary = %s,
                                            ecsg = %s,
                                            elevy = %s,
                                            ensf = %s,
                                            prgf = %s,
                                            csg = %s,
                                            nsf = %s,
                                            slevy = %s,
                                            paye = %s
                                            WHERE
                                            UNQ = %s;
                                            """
                            contri_data = [eid, lname, fname, basic, enps, levy, ensf, eprgf, nps, nsf, slevypay, paye, UNQ]
                            cursor.execute(update_contri, contri_data)
                            print("Update Contribution Complete")

                        msg = "Re-Processing Complete For " + flname + " "
                        print(msg)
                
                if msg == "Employee Not Working":
                    get_empid = "SELECT EmployeeID FROM salary WHERE UNQ = %s"
                    cursor.execute(get_empid, data3)
                    emp_id = cursor.fetchall()
                    msg = "Employee Not Working , Re Processing Complete"

                    if emp_id != []:
                        print("In Delete Employee")
                        delete_original = "DELETE FROM OriginalData WHERE UNQ = %s"
                        cursor.execute(delete_original,data3)
                        print("Delete From Original Data")

                        delete_salary = "DELETE FROM salary WHERE UNQ= %s"
                        cursor.execute(delete_salary,data3)
                        print("Delete From Salary Data")
                        
                        delete_payslip = "DELETE FROM payslip WHERE UNQ = %s"
                        cursor.execute(delete_payslip,data3)
                        print("Delete From Payslip Data")
                        
                        delete_paye = "DELETE FROM payecsv WHERE UNQ = %s"
                        cursor.execute(delete_paye,data3)
                        print("Delete From Payecsv Data")
                        
                        delete_prgf = "DELETE FROM prgfcsv WHERE UNQ = %s "
                        cursor.execute(delete_prgf,data3)
                        print("Delete From PRGF Data")
                        
                        delete_cnp = "DELETE FROM cnpcsv WHERE UNQ = %s"
                        cursor.execute(delete_cnp,data3)
                        print("Delete From CNP Data")
                        
                        delete_contri = "DELETE FROM contribution WHERE UNQ = %s"
                        cursor.execute(delete_contri,data3)
                        print("Delete From Contribution Data")

                query15 = "SELECT Basic FROM cnpcsv WHERE month = %s"
                data7 = [month]
                cursor.execute(query15, data7)
                basic_sal = cursor.fetchall()

                temp1 = []
                temp2 = []
                for i in range(len(basic_sal)):
                    temp1 = ''.join(basic_sal[i])
                    temp2.append(temp1)
                total = 0
                for i in range(len(temp2)):
                    total = int(total) + int(temp2[i]) 

                cnp = round(int(total) * 0.015)
                
                update_cnp = """UPDATE cnpcsv
                SET 
                totalRem = %s,
                CNP = %s
                WHERE
                month = %s;"""
                data8 = [total, cnp, month]
                cursor.execute(update_cnp, data8)
# =================================================================================================================================

                query16 = "SELECT Salary FROM contribution WHERE month = %s"
                cursor.execute(query16, data7)
                basic_con = cursor.fetchall()

                bas1 = []
                bas2 = []

                for i in range(len(basic_con)):
                    bas1 = ''.join(basic_con[i])
                    bas2.append(bas1)
                bas_total = 0

                for i in range(len(bas2)):
                    bas_total = int(bas_total) + int(bas2[i])

# =================================================================================================================================

                query17 = "SELECT ecsg FROM contribution WHERE month = %s"
                cursor.execute(query17, data7)
                ecsg_con = cursor.fetchall()

                ecsg1 = []
                ecsg2 = []

                for i in range(len(ecsg_con)):
                    ecsg1 = ''.join(ecsg_con[i])
                    ecsg2.append(ecsg1)
                ecsg_total = 0

                for i in range(len(ecsg2)):
                    ecsg_total = int(ecsg_total) + int(ecsg2[i])

# =================================================================================================================================

                query18 = "SELECT elevy FROM contribution WHERE month = %s"
                cursor.execute(query18, data7)
                elevy_con = cursor.fetchall()

                elevy1 = []
                elevy2 = []

                for i in range(len(elevy_con)):
                    elevy1 = ''.join(elevy_con[i])
                    elevy2.append(elevy1)
                elevy_total = 0

                for i in range(len(elevy2)):
                    elevy_total = int(elevy_total) + int(elevy2[i])

# =================================================================================================================================

                query19 = "SELECT ensf FROM contribution WHERE month = %s"
                cursor.execute(query19, data7)
                ensf_con = cursor.fetchall()

                ensf1 = []
                ensf2 = []

                for i in range(len(ensf_con)):
                    ensf1 = ''.join(ensf_con[i])
                    ensf2.append(ensf1)
                ensf_total = 0

                for i in range(len(ensf2)):
                    ensf_total = int(ensf_total) + int(ensf2[i])

# =================================================================================================================================

                query23 = "SELECT prgf FROM contribution WHERE month = %s"
                cursor.execute(query23, data7)
                prgf_con = cursor.fetchall()

                prgf1 = []
                prgf2 = []

                for i in range(len(prgf_con)):
                    prgf1 = ''.join(prgf_con[i])
                    prgf2.append(prgf1)
                prgf_total = 0

                for i in range(len(prgf2)):
                    prgf_total = int(prgf_total) + int(prgf2[i])                    

# =================================================================================================================================

                query20 = "SELECT csg FROM contribution WHERE month = %s"
                cursor.execute(query20, data7)
                csg_con = cursor.fetchall()

                csg1 = []
                csg2 = []

                for i in range(len(csg_con)):
                    csg1 = ''.join(csg_con[i])
                    csg2.append(csg1)
                csg_total = 0

                for i in range(len(csg2)):
                    csg_total = int(csg_total) + int(csg2[i])

# =================================================================================================================================

                query21 = "SELECT nsf FROM contribution WHERE month = %s"
                cursor.execute(query21, data7)
                nsf_con = cursor.fetchall()

                nsf1 = []
                nsf2 = []

                for i in range(len(nsf_con)):
                    nsf1 = ''.join(nsf_con[i])
                    nsf2.append(nsf1)
                nsf_total = 0

                for i in range(len(nsf2)):
                    nsf_total = int(nsf_total) + int(nsf2[i])

# =================================================================================================================================

                query22 = "SELECT slevy FROM contribution WHERE month = %s"
                cursor.execute(query22, data7)
                slevy_con = cursor.fetchall()

                slevy1 = []
                slevy2 = []

                for i in range(len(slevy_con)):
                    slevy1 = ''.join(slevy_con[i])
                    slevy2.append(slevy1)
                slevy_total = 0

                for i in range(len(slevy2)):
                    slevy_total = int(slevy_total) + int(slevy2[i])

# =================================================================================================================================

                query24 = "SELECT paye FROM contribution WHERE month = %s"
                cursor.execute(query24, data7)
                paye_con = cursor.fetchall()

                paye1 = []
                paye2 = []

                for i in range(len(paye_con)):
                    paye1 = ''.join(paye_con[i])
                    paye2.append(paye1)
                paye_total = 0

                for i in range(len(paye2)):
                    paye_total = int(paye_total) + int(paye2[i])                    

# =================================================================================================================================

                update_contri = """UPDATE contribution
                SET
                totalRem = %s,
                totalecsg = %s,
                totalelevy = %s,
                totalensf = %s,
                totalprgf = %s,
                totalcsg = %s,
                totalnsf = %s,
                totalslevy = %s,
                totalpaye = %s
                WHERE 
                month = %s;
                """

                update_contri_data = [bas_total, ecsg_total, elevy_total, ensf_total, prgf_total, csg_total, nsf_total, slevy_total, paye_total, month]

                cursor.execute(update_contri, update_contri_data)

                print("Contribution Update Complete")

                return render_template("process.html", msg=msg)

# =================================================================================================================== #

# ========================================== For Employee ID "ALL" ================================================== #

# =================================================================================================================== #

            elif eid == "ALL":                 
                # print(month)
                month = request.form["mon"]
        
                year = request.form["year"]

                cur_date = date.today()

                res = calendar.monthrange(cur_date.year, cur_date.month)
                day = res[1]
                
                # print(day)

                # print(cur_date)
                # print(type(cur_date))
                # print(type(str(cur_date)))

                cur_date = str(cur_date)

                id = 0
                month = month.lower()          
                if month == "January" or month=="january":
                    print("In Jan")
                    
                    id = 1
                elif month == "February" or month=="february":
                    print("In Feb")
                    
                    current_date = "2022-"+"02-"+"31"
                    id = 2
                elif month == "March" or month=="march":
                    print("In Mar")
                    
                    current_date = "2022-"+"03-"+"31"
                    id = 3
                elif month == "April" or month=="april":
                    print("In Apr")
                    
                    current_date = "2022-"+"04-"+"31"
                    id = 4
                elif month == "May" or month=="may":
                    print("In May")
                    
                    current_date = "2022-"+"05-"+"31"
                    id = 5
                elif month == "June" or month=="june":
                    print("In Jun")
                    
                    current_date = "2022-"+"06-"+"31"
                    id = 6
                elif month == "July" or month=="july":
                    print("In Jul")
                    
                    current_date = "2022-"+"07-"+"31"
                    id = 7
                elif month == "August" or month=="august":
                    print("In Aug")
                    
                    current_date = "2022-"+"08-"+"31"
                    id = 8
                elif month == "September" or month=="september":
                    print("In Sep")
                    
                    current_date = "2022-"+"09-"+"31"
                    id = 9
                elif month == "October" or month=="october":
                    print("In Oct")
                    
                    current_date = "2022-"+"10-"+"31"
                    id = 10
                elif month == "November" or month=="november":
                    print("In Nov")
                    
                    current_date = "2022-"+"11-"+"31"
                    id = 11
                elif month == "December" or month=="december":
                    print("In Dec")

                    current_date = "2022-"+"12-"+"31"
                    id = 12
                else:  
                    print("In Else")
                    msg = "Enter Month Correctly"
                    return render_template("process.html", msg = msg)
                mid = id-1
                if mid == 0:
                    mid = 12
                
                # print(calendar.month_name[id])
                month2 = calendar.month_name[mid]
                month2 = month2.lower()

                # query3 = "SELECT Carbenefit, salary, Fixedallow, Travelallow, EDF, Educationrel, Medicalrel, medical, Specialbonus FROM employee WHERE EmployeeID = %s "
                # query3 = "SELECT Carbenefit, salary, Fixedallow, Travelallow, EDF, Educationrel, Medicalrel, medical, Specialbonus, EmployeeID FROM employee"
                query = "SELECT Carbenefit, salary, Fixedallow, Travelallow, EDF, Educationrel, Medicalrel, Medicalrel, Specialbonus, EmployeeID, months FROM employee"
                # cursor.execute(query3, data)
                cursor.execute(query)
                emp_data = cursor.fetchall()

                # print(emp_data)

                arrays = {}
                for index,lst in enumerate(emp_data):
                    arrays[str(index+1)] = lst
                # print(arrays)
                msg = ""
                for i in arrays:
                    # print(i)
                    emp_data2 = list(arrays[i])
                    # emp_data2 = list(emp_data[0])

                    car = int(emp_data2[0])
                    # print(car)
                    # print(type(car))
                    
                    tbasic = int(emp_data2[1])
                    fixAllow = int(emp_data2[2])
                    trans = int(emp_data2[3])
                    edf = int(emp_data2[4])
                    education = int(emp_data2[5])
                    Medicalrel = int(emp_data2[6])
                    # temp_medical = int(emp_data2[7])
                    medical = round(int(Medicalrel) / 12)
                    # medical = 0
                    SpeProBns = int(emp_data2[8])
                    eid = emp_data2[9]
                    month_count = int(emp_data2[10])

                    # lwork = emp_data2[10]
                    # print(lwork)

                    data = [eid]
                    data2 = [eid,month2]
                    # print(month2)

                    query_month = "SELECT MONTH(Lastwork) AS Month FROM employee WHERE EmployeeID= %s"
                    cursor.execute(query_month, data)
                    emp_month = cursor.fetchall()
                    
                    last_mon = emp_month[0][0]
                    
                    query_year = "SELECT YEAR(Lastwork) AS Year FROM employee WHERE EmployeeID= %s"
                    cursor.execute(query_year, data)
                    emp_year = cursor.fetchall()

                    last_year = emp_year[0][0]

                    msg = "Processing Complete"

                    hire_date = "SELECT hire FROM employee WHERE EmployeeID = %s"
                    cursor.execute(hire_date, data)
                    hire_date_emp = cursor.fetchall()
                    
                    print(hire_date_emp)
                    hire_dt = str(hire_date_emp[0][0])

                    pension_query = "SELECT NPS FROM employee WHERE EmployeeID= %s"
                    cursor.execute(pension_query , data)
                    pension = cursor.fetchall()

                    pension = pension[0][0]

                    expatriate_query = "SELECT expatriate FROM employee WHERE EmployeeID = %s"
                    cursor.execute(expatriate_query, data)
                    expatriate = cursor.fetchall()

                    expatriate = expatriate[0][0]
                    
                    if (int(last_year) >= int(year) or (last_year == 1 and last_mon == 1)) and (hire_dt <= cur_date):
                        print("Year Is Correct ", eid)
                        if int(last_mon) >= int(id) or (last_year == 1 and last_mon == 1):
                            print("In Start Process")
                            query1 = "SELECT FirstName FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query1,data)
                            fname = cursor.fetchall()
                            for i in range(len(fname)):
                                fname = ''.join(fname[i])

                            query2 = "SELECT LastName FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query2,data)
                            lname = cursor.fetchall()
                            for i in range(len(lname)):
                                lname = ''.join(lname[i])

                            query3 = "SELECT cGrossTax FROM salary WHERE EmployeeID= %s AND Month = %s"
                            cursor.execute(query3,data2)
                            prevGross = cursor.fetchall()
                            for i in range(len(prevGross)):
                                if prevGross != None:
                                    prevGross = ''.join(prevGross[i])
                                else:
                                    prevGross = 0
                            if prevGross != 0:
                                prevGross = ''.join(map(str,prevGross))
                                

                            query4 = "SELECT IET FROM salary WHERE EmployeeID= %s AND Month = %s"
                            cursor.execute(query4,data2)
                            piet = cursor.fetchall()
                            for i in range(len(piet)):
                                if piet != None:
                                    piet = ''.join(piet[i])
                                else:
                                    piet = 0
                            if piet != 0:
                                piet = ''.join(map(str,piet))

                            query5 = "SELECT CurrentPAYE FROM salary WHERE EmployeeID= %s AND Month = %s"
                            cursor.execute(query5,data2)
                            ppaye = cursor.fetchall()
                            # print(ppaye)
                            for i in range(len(ppaye)):
                                if ppaye != None:
                                    ppaye = ''.join(ppaye[i])
                                else:
                                    ppaye = 0
                            if ppaye != 0:
                                ppaye = ''.join(map(str,ppaye))

                            query6 = "SELECT Threshold FROM salary WHERE EmployeeID= %s AND Month = %s"
                            cursor.execute(query6,data2)
                            pths = cursor.fetchall()
                            for i in range(len(pths)):
                                if pths != None:
                                    pths = ''.join(pths[i])
                                else:
                                    pths = 0
                            if pths != 0:
                                pths = ''.join(map(str,pths))

                            query7 = "SELECT CurrentSLevy FROM salary WHERE EmployeeID= %s AND Month = %s"
                            cursor.execute(query7,data2)
                            plevy = cursor.fetchall()

                            if len(plevy) > 0:
                                for i in range(len(plevy)):
                                    plevy = ''.join(plevy[i])
                            else:
                                plevy = 0    


                            # for i in range(len(plevy)):
                            #     print("In For")
                            #     if plevy != None:
                            #         print("In if1")
                            #         plevy = ''.join(plevy[i])
                            #     else:
                            #         print("In Else")
                            #         plevy = 0
                            
                            # if plevy != 0:
                            #     print("In if2")
                            #     plevy = ''.join(map(str,plevy))
                            

                            query8 = "SELECT hire FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query8,data)
                            hire = cursor.fetchall()
                            
                            hire = hire[0][0] 
                            hire = str(hire)
                            # print(hire)
                            # print(str(hire))
                            # print(type(str(hire)))
                            # if hire != None:
                            #     for i in range(len(hire)):
                            #         hire = ''.join(hire[i])
                            #     hire = ''.join(map(str,hire))
                            # else:
                            #     hire = 0                    

                            query9 = "SELECT position FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query9,data)
                            pos = cursor.fetchall()
                            for i in range(len(pos)):
                                if pos != None:
                                    pos = ''.join(pos[i])
                                else:
                                    pos = " "
                            if pos != 0:
                                pos = ''.join(map(str,pos))
                            # print(pos)
                            

                            query10 = "SELECT NICno FROM employee WHERE EmployeeID = %s"
                            cursor.execute(query10,data)
                            nic = cursor.fetchall()
                            # print(nic)
                            for i in range(len(nic)):
                                if nic[0][0] != None:
                                    nic = ''.join(nic[i])
                                else:
                                    nic = " "
                            if nic != 0:
                                nic = ''.join(map(str,nic))
                            
                            UNQ = month + " " + fname
                            data3 = [UNQ]
                            
                            # query11 = "SELECT LockSal From salary WHERE UNQ = %s"
                            # cursor.execute(query11,data3)
                            # lockSal = cursor.fetchall()

                            # print(lockSal)
                            # print(len(lockSal))

                            # if len(lockSal) > 0:
                            #     print("In If")
                            #     for i in range(len(lockSal)):
                            #         print("In For ")
                            #         lockSal = ''.join(lockSal[i])
                            # else:
                            #     print("In Else")
                            #     lockSal = "No"

                            query11 = "SELECT ProcSal From salary WHERE UNQ = %s"
                            cursor.execute(query11,data3)
                            ProcSal = cursor.fetchall()

                            if len(ProcSal) > 0:
                                for i in range(len(ProcSal)):
                                    ProcSal = ''.join(ProcSal[i])
                            else:
                                ProcSal = "No"

                            # query12 = "SELECT working FROM employee WHERE EmployeeID = %s"
                            # cursor.execute(query12, data)
                            # working = cursor.fetchall()

                            # if len(working) > 0:
                            #     print("In If")
                            #     for i in range(len(working)):
                            #         print("In For ")
                            #         working = ''.join(working[i])
                            # else:
                            #     print("In Else")
                            #     working = "Yes"
                            

                            if ProcSal == "No":                        
                                if pension == 'Paid':
                                    flname = lname + " " + fname

                                    # Values We Don't Get
                                    ot = 0
                                    otherAllow = 0
                                    arrears = 0
                                    eoy = 0
                                    leave = 0
                                    speBns = 0
                                    discBns = 0
                                    tax = 0
                                    ntax = 0
                                    attBns = 0
                                    overseas = tax + ntax

                                    loan = 0
                                    lateness = 0
                                    otherDed = 0
                                    ab = 0

                                    # Previous Data
                                    # print(type(prevGross))
                                    # print(prevGross)
                                    if prevGross == "":
                                        prevGross = 0
                                    else:
                                        prevGross = int(prevGross)

                                    if piet == "":
                                        piet = 0
                                    else:
                                        piet = int(piet)
                                    
                                    if ppaye == "":
                                        ppaye = 0
                                    else:
                                        ppaye = int(ppaye)
                                    
                                    if pths == "":
                                        pths = 0
                                    else:
                                        pths = int(pths)
                                    # print(pths)
                                    if plevy == "":
                                        plevy = 0
                                    else:
                                        plevy = int(plevy)
                            
                                    basic = int(tbasic) - int(ab)
                                    # Calculations
                                    payable = basic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns
                                    bonus = speBns + SpeProBns + otherAllow + fixAllow + discBns + attBns

                                    pay_gross = tbasic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns

                                    # For Overseas Amount
                                    if overseas > 0:
                                        ntax = round(int(basic) * 0.06)
                                        tax = round(int(overseas) - int(ntax))
                                    else:
                                        ntax = 0
                                        tax = 0

                                    if trans > 20000:
                                        transTax = trans - 20000
                                        ntransTax = trans - transTax
                                    else:
                                        transTax = 0
                                        ntransTax = trans

                                    cgross = basic + ot + otherAllow + trans + arrears + eoy + leave + discBns + fixAllow + tax + SpeProBns + attBns + car

                                    grossTax = basic + ot + transTax +otherAllow + arrears + eoy + leave + discBns + fixAllow  + tax + SpeProBns + attBns + car

                                    # print("prev Gross " , prevGross)
                                    # print("Curr Gross " , cgross)
                                    gross = prevGross + grossTax
                                    # print("gross" , gross)
                                    medf = round(int(edf) / int(month_count))
                                    ciet = round(( int(edf) + int(Medicalrel) + int(education)) / int(month_count))
                                    
                                    iet = int(ciet) + int(piet)
                                    # print("ciet" , ciet)
                                    # print("piet", piet)
                                    # print("iet", iet)

                                    netch = gross - iet

                                    # print("netch" , netch)
                                    if netch < 0:
                                        netch = 0
                                    else:
                                        netch = netch

                                    if int(basic) > 50000:
                                        nps = round(basic * 0.03)
                                        # cpaye =  round(netch * 0.15)
                                        enps = round(basic * 0.06)
                                    else:
                                        nps = round(basic * 0.015)
                                        # cpaye = round(netch * 0.1)
                                        enps = round(basic * 0.03)

                                    check = int(basic) + int(otherAllow) - int(medf)
                                    if check < 53846:
                                        cpaye = round(netch* 0.1)
                                    elif check >= 53846 and check < 75000:
                                        cpaye = round(netch* 0.125)
                                    else:
                                        cpaye = round(netch* 0.15)

                                    if cpaye < 0:
                                        cpaye = 0
                                    else:
                                        cpaye = int(cpaye)
                                    
                                    if ppaye < 0:
                                        ppaye =0
                                    else:
                                        ppaye = int(ppaye)

                                    # print("cpaye", cpaye)
                                    # print("ppaye", ppaye)
                                    paye = int(cpaye) - int(ppaye)
                                    # print("paye", paye)
                                    if paye < 0:
                                        paye =0
                                    else:
                                        paye = int(paye)

                                    nsf = int(basic * 0.01)

                                    if nsf > 214:
                                        nsf = 214
                                    else:
                                        nsf = int(nsf)

                                    temp = int(cgross) * 13
                                    slevy = 0
                                    tths = round(3000000/12)
                                    ths = int(pths) + int(tths)
                                    # print(ths)
                                    netchar = int(gross) - int(iet) - int(ths)
                                
                                    if netchar < 0 :
                                        netchar = 0
                                    else:
                                        netchar = netchar

                                    if int(temp) > 3000000:
                                        slevy1 = round(netchar * 0.25)
                                        slevy2 = round(gross * 0.1)
                                        
                                        if slevy1 > slevy2:
                                            slevy = int(slevy2)
                                        else:
                                            slevy = int(slevy1)
                                    else:
                                        slevy = 0
                                    
                                    ensf = round(basic * 0.025)
                                    if ensf > 536:
                                        ensf = 536
                                    else:
                                        ensf = round(ensf)
                                    levy = round(int(basic) * 0.015)
                                    deduction = int(loan) + int(paye) + int(lateness) + int(nps) + int(otherDed) + int(nsf) + int(medical)
                                    net = int(payable) - int(deduction)
                                    # print(slevy)
                                    
                                    slevypay = slevy - plevy
                                    NetPaysheet = int(net) - int(slevypay)
                                    
                                    otherAllow2 = int(otherAllow) 
                                    
                                    tax = int(tax) + int(transTax)
                                    ntax = int(ntax) + int(ntransTax)
                                    # Payslip Calculation

                                    paygross = int(basic) + int(trans) + int(bonus)

                                    totalDeduction = int(paye) + int(nps) + int(nsf) + int(slevypay)

                                    netpay = paygross - totalDeduction
                                    # eprgf = 0
                                    if expatriate == "No":
                                        if basic < 200000:
                                            eprgf = round((int(basic) + int(bonus)) * 0.035) # + commission
                                        else:
                                            eprgf = 0
                                    else:
                                        eprgf = 0

# ===============================================================================================================================================================================================

                                else:
                                        # Values We Don't Get
                                    ot = 0
                                    otherAllow = 0
                                    arrears = 0
                                    eoy = 0
                                    leave = 0
                                    speBns = 0
                                    discBns = 0
                                    tax = 0
                                    ntax = 0
                                    attBns = 0
                                    overseas = tax + ntax

                                    loan = 0
                                    lateness = 0
                                    otherDed = 0
                                    ab = 0

                                    # Previous Data
                                    # print(type(prevGross))
                                    # print(prevGross)
                                    prevGross = 0
                                    piet = 0
                                    ppaye = 0
                                    pths = 0
                                    plevy = 0
                            
                                    basic = int(tbasic) - int(ab)
                                    # Calculations
                                    payable = basic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns
                                    bonus = speBns + SpeProBns + otherAllow + fixAllow + discBns + attBns

                                    pay_gross = tbasic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns

                                    # For Overseas Amount
                                    if overseas > 0:
                                        ntax = round(int(basic) * 0.06)
                                        tax = round(int(overseas) - int(ntax))
                                    else:
                                        ntax = 0
                                        tax = 0

                                    if trans > 20000:
                                        transTax = trans - 20000
                                        ntransTax = trans - transTax
                                    else:
                                        transTax = 0
                                        ntransTax = trans

                                    cgross = basic + ot + otherAllow + trans + arrears + eoy + leave + discBns + fixAllow + tax + SpeProBns + attBns + car

                                    grossTax = basic + ot + transTax +otherAllow + arrears + eoy + leave + discBns + fixAllow  + tax + SpeProBns + attBns + car

                                    # print("prev Gross " , prevGross)
                                    # print("Curr Gross " , cgross)
                                    gross = prevGross + grossTax
                                    # print("gross" , gross)
                                    medf = round(int(edf) / int(month_count))
                                    ciet = round(( int(edf) + int(Medicalrel) + int(education)) / int(month_count))
                                    
                                    iet = int(ciet) + int(piet)
                                    # print("ciet" , ciet)
                                    # print("piet", piet)
                                    # print("iet", iet)

                                    netch = gross - iet

                                    # print("netch" , netch)
                                    if netch < 0:
                                        netch = 0
                                    else:
                                        netch = netch

                                    nps = 0
                                    enps = 0
                                    cpaye = 0
                                    ppaye = 0
                                    
                                    paye = int(cpaye) - int(ppaye)
                                    # print("paye", paye)
                                    if paye < 0:
                                        paye =0
                                    else:
                                        paye = int(paye)

                                    nsf = 0
                                    # nsf = int(basic * 0.01)

                                    # if nsf > 214:
                                    #     nsf = 214
                                    # else:
                                    #     nsf = int(nsf)

                                    temp = int(cgross) * 13
                                    slevy = 0
                                    tths = round(3000000/12)
                                    ths = int(pths) + int(tths)
                                    # print(ths)
                                    netchar = int(gross) - int(iet) - int(ths)
                                
                                    if netchar < 0 :
                                        netchar = 0
                                    else:
                                        netchar = netchar

                                    slevy = 0

                                    # if int(temp) > 3000000:
                                    #     slevy1 = round(netchar * 0.25)
                                    #     slevy2 = round(gross * 0.1)
                                        
                                    #     if slevy1 > slevy2:
                                    #         slevy = int(slevy2)
                                    #     else:
                                    #         slevy = int(slevy1)
                                    # else:
                                    #     slevy = 0
                                    
                                    ensf = 0
                                    # ensf = round(basic * 0.025)
                                    # if ensf > 536:
                                    #     ensf = 536
                                    # else:
                                    #     ensf = round(ensf)

                                    levy = 0
                                    # levy = round(int(basic) * 0.015)

                                    deduction = int(loan) + int(paye) + int(lateness) + int(nps) + int(otherDed) + int(nsf) + int(medical)
                                    net = int(payable) - int(deduction)
                                    # print(slevy)
                                    
                                    slevypay = slevy - plevy
                                    NetPaysheet = int(net) - int(slevypay)
                                    
                                    otherAllow2 = int(otherAllow) 
                                    
                                    tax = int(tax) + int(transTax)
                                    ntax = int(ntax) + int(ntransTax)
                                    # Payslip Calculation

                                    paygross = int(basic) + int(trans) + int(bonus)

                                    totalDeduction = int(paye) + int(nps) + int(nsf) + int(slevypay)

                                    netpay = paygross - totalDeduction
                                    eprgf = 0
                                    # if basic < 200000:
                                    #     eprgf = round((int(basic) + int(bonus)) * 0.035) # + commission
                                    # else:
                                    #     eprgf = 0

                                insert_query = """
                                INSERT INTO OriginalData(
                                EmployeeID,
                                EmployeeName,
                                BasicSalary,
                                FixedAllow,
                                OtherDeduction,
                                Overtime,
                                DiscBonus,
                                NSFEmpee,
                                OtherAllow,
                                TaxableAllow,
                                Medical,
                                Transport,
                                overseas,
                                NTaxableAllow,
                                EDF,
                                Arrears,
                                AttendanceBns,
                                EOY,
                                Loan,
                                CarBenefit,
                                LeaveRef,
                                SLevy,
                                SpecialBns,
                                Lateness,
                                EducationRel,                    
                                SpeProBns,
                                NPS,
                                MedicalRel,
                                Payable,
                                Deduction,
                                NetPay,
                                NetPaysheet,
                                paysheet_gross,
                                CurrentGross,
                                cGrossTax,
                                PrevGross,
                                PrevIET,
                                IET,
                                NetCh,
                                CurrentPAYE,
                                PrevPAYE,
                                PAYE,
                                eCSG,
                                eNSF,
                                eLevy,
                                PRGF,
                                PrevThreshold,
                                Threshold,
                                netchar,
                                CurrentSLevy,
                                PrevSLevy,
                                slevyPay,
                                Absences,
                                Month,
                                Year,
                                UNQ,
                                LockSal
                                )

                                VALUES(
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                                );
                                """
                                data_original = [eid, flname, basic , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoy, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, pay_gross, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, month, year, UNQ, 'No']
                                cursor.execute(insert_query, data_original)
                                print("Process Query Executed")

                                insert_query2 = """
                                INSERT INTO salary(
                                EmployeeID,
                                EmployeeName,
                                BasicSalary,
                                FixedAllow,
                                OtherDeduction,
                                Overtime,
                                DiscBonus,
                                NSFEmpee,
                                OtherAllow,
                                TaxableAllow,
                                Medical,
                                Transport,
                                overseas,
                                NTaxableAllow,
                                EDF,
                                Arrears,
                                AttendanceBns,
                                EOY,
                                Loan,
                                CarBenefit,
                                LeaveRef,
                                SLevy,
                                SpecialBns,
                                Lateness,
                                EducationRel,                    
                                SpeProBns,
                                NPS,
                                MedicalRel,
                                Payable,
                                Deduction,
                                NetPay,
                                NetPaysheet,
                                paysheet_gross,
                                CurrentGross,
                                cGrossTax,
                                PrevGross,
                                PrevIET,
                                IET,
                                NetCh,
                                CurrentPAYE,
                                PrevPAYE,
                                PAYE,
                                eCSG,
                                eNSF,
                                eLevy,
                                PRGF,
                                PrevThreshold,
                                Threshold,
                                netchar,
                                CurrentSLevy,
                                PrevSLevy,
                                slevyPay,
                                Absences,
                                Month,
                                Year,
                                UNQ,
                                LockSal,
                                ProcSal
                                )

                                VALUES(
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                                );
                                """
                                data_salary = [eid, flname, basic , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoy, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, pay_gross , cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, month, year, UNQ, 'No', 'Yes']
                                cursor.execute(insert_query2, data_salary)
                                print("Process Query Executed")


                                query = """INSERT INTO payslip(
                                        JoinDate,
                                        Company,
                                        EmpName,
                                        Position,
                                        NIC,
                                        BasicSalary,
                                        TravelAlw,
                                        Bonus,
                                        Gross,
                                        PAYE,
                                        NPF,
                                        NSF,
                                        SLevy,
                                        Deduction,
                                        NetPay,
                                        Payable,
                                        NetPayAcc,
                                        eNPF,
                                        eNSF,
                                        eLevy,
                                        ePRGF,
                                        month,
                                        year,
                                        UNQ
                                        )
                                        VALUES(
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s,
                                        %s
                                        );
                                        """
                                
                                data_payslip = [hire, "CARE Ratings (Africa) Private Limitedivate Limited" , flname, pos, nic, basic, trans, bonus, paygross, paye, nps, nsf, slevypay , totalDeduction, netpay,netpay, netpay, enps, ensf, levy, eprgf, month, year, UNQ ]
                                cursor.execute(query, data_payslip)
                                print("Payslip Query Executed")
                                

                                query14 = "SELECT NICno FROM employee WHERE EmployeeID = %s"
                                cursor.execute(query14, data)
                                nic = cursor.fetchall()
                                if nic[0][0] == "":
                                    nic = " "
                                else:
                                    for i in range(len(nic)):
                                        nic = ''.join(nic[i])
                                
                                    
                                emolument = int(basic) + int(arrears) + int(overseas) + int(otherAllow) + int(car) + int(ot) + int(eoy) + int(leave) + int(fixAllow) + int(discBns) + int(SpeProBns) + int(speBns) 

                                query12 = "SELECT NPS FROM employee WHERE EmployeeID = %s"
                                cursor.execute(query12, data)
                                pension = cursor.fetchall()
                                for i in range(len(pension)):
                                    pension = ''.join(pension[i])

                                if pension == "Paid":
                                    pension = "Yes"
                                else:
                                    pension = "No"

                                query13 = "SELECT working FROM employee WHERE EmployeeID = %s"
                                cursor.execute(query13, data)
                                working = cursor.fetchall()
                                for i in range(len(working)):
                                    working = ''.join(working[i])
                                
                                # query14 = "SELECT NICno FROM employee WHERE EmployeeID = %s"
                                # cursor.execute(query14, data)
                                # nic = cursor.fetchall()
                                # for i in range(len(nic)):
                                #     nic = ''.join(nic[i])

                                allowance = int(otherAllow) + int(fixAllow) + int(speBns) + int(SpeProBns) + int(discBns) + int(attBns)
                                commission = 0

                                totalRem = int(basic) + int(allowance)

                                if expatriate == "No":

                                    paye_query = """ INSERT INTO payecsv(
                                                EmployeeID,
                                                LastName,
                                                FirstName,
                                                Emoluments,
                                                PAYE,
                                                working,
                                                SLevy,
                                                EmolumentsNet,
                                                month,
                                                UNQ
                                                )
                                                VALUES(
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s,
                                                    %s
                                                );"""
                                    data_paye = [nic, lname, fname, emolument, paye, 'Yes', slevypay, emolument, month, UNQ]

                                    cursor.execute(paye_query, data_paye)
                                    print("PAYE Query Executed")
                                    
                                    prgf_query = """INSERT INTO prgfcsv(
                                                EmployeeID,
                                                LastName,
                                                FirstName,
                                                Pension,
                                                Working,
                                                Hire,
                                                Basic,
                                                Allowance,
                                                Commission,
                                                TotalRem,
                                                PRGF,
                                                reason,
                                                month,
                                                UNQ
                                                )
                                                VALUES(
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s
                                                );"""
                                    if basic < 200000:
                                        data_prgf = [nic, lname, fname, "No", working, hire, basic, allowance, commission, totalRem, eprgf, " " , month, UNQ]
                                    else:
                                        data_prgf = [nic, lname, fname, "No", working, hire, basic, 0, 0, 0, 0, " " , month, UNQ]
                                    
                                    cursor.execute(prgf_query, data_prgf)

                                    cnp_query = """INSERT INTO cnpcsv(
                                            EmployeeID,
                                            LastName,
                                            FirstName,
                                            Basic,
                                            Basic2,
                                            Season,
                                            Alphabet,
                                            Number,
                                            Working,
                                            Blank1,
                                            Blank2,
                                            month,
                                            UNQ
                                            )
                                            VALUES(
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s
                                            );"""
                                    data_cnp = [nic, lname, fname, basic, basic, "S2", "M", "1", working, " ", " ", month, UNQ]

                                    cursor.execute(cnp_query, data_cnp)
                                    print("CNP Insert Query Executed")

                                insert_contri = """INSERT INTO contribution(
                                                EmployeeID,
                                                LastName,
                                                FirstName,
                                                IDCard,
                                                Salary,
                                                blank1,
                                                ecsg,
                                                elevy,
                                                ensf,
                                                prgf,
                                                csg,
                                                nsf,
                                                slevy,
                                                paye,
                                                month,
                                                year,
                                                UNQ
                                                )
                                                VALUES(
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s
                                                );
                                                """
                                contri_data = [eid, lname, fname, nic, basic, " ", enps, levy, ensf, eprgf, nps, nsf, slevypay, paye, month, year, UNQ]
                                cursor.execute(insert_contri, contri_data)
                                print("Contribution Insert Executed")
                                msg = "Processing Complete"
                                # print("Do Something Else")

                        query15 = "SELECT Basic FROM cnpcsv WHERE month = %s"
                        data7 = [month]
                        cursor.execute(query15, data7)
                        basic_sal = cursor.fetchall()

                        temp1 = []
                        temp2 = []
                        for i in range(len(basic_sal)):
                            temp1 = ''.join(basic_sal[i])
                            temp2.append(temp1)
                        total = 0
                        for i in range(len(temp2)):
                            total = int(total) + int(temp2[i]) 

                        cnp = round(int(total) * 0.015)
                        
                        update_cnp = """UPDATE cnpcsv
                        SET 
                        totalRem = %s,
                        CNP = %s
                        WHERE
                        month = %s;"""
                        data8 = [total, cnp, month]
                        cursor.execute(update_cnp, data8)
        # =================================================================================================================================

                        query16 = "SELECT Salary FROM contribution WHERE month = %s"
                        cursor.execute(query16, data7)
                        basic_con = cursor.fetchall()

                        bas1 = []
                        bas2 = []

                        for i in range(len(basic_con)):
                            bas1 = ''.join(basic_con[i])
                            bas2.append(bas1)
                        bas_total = 0

                        for i in range(len(bas2)):
                            bas_total = int(bas_total) + int(bas2[i])

        # =================================================================================================================================

                        query17 = "SELECT ecsg FROM contribution WHERE month = %s"
                        cursor.execute(query17, data7)
                        ecsg_con = cursor.fetchall()

                        ecsg1 = []
                        ecsg2 = []

                        for i in range(len(ecsg_con)):
                            ecsg1 = ''.join(ecsg_con[i])
                            ecsg2.append(ecsg1)
                        ecsg_total = 0

                        for i in range(len(ecsg2)):
                            ecsg_total = int(ecsg_total) + int(ecsg2[i])

        # =================================================================================================================================

                        query18 = "SELECT elevy FROM contribution WHERE month = %s"
                        cursor.execute(query18, data7)
                        elevy_con = cursor.fetchall()

                        elevy1 = []
                        elevy2 = []

                        for i in range(len(elevy_con)):
                            elevy1 = ''.join(elevy_con[i])
                            elevy2.append(elevy1)
                        elevy_total = 0

                        for i in range(len(elevy2)):
                            elevy_total = int(elevy_total) + int(elevy2[i])

        # =================================================================================================================================

                        query19 = "SELECT ensf FROM contribution WHERE month = %s"
                        cursor.execute(query19, data7)
                        ensf_con = cursor.fetchall()

                        ensf1 = []
                        ensf2 = []

                        for i in range(len(ensf_con)):
                            ensf1 = ''.join(ensf_con[i])
                            ensf2.append(ensf1)
                        ensf_total = 0

                        for i in range(len(ensf2)):
                            ensf_total = int(ensf_total) + int(ensf2[i])

        # =================================================================================================================================

                        query23 = "SELECT prgf FROM contribution WHERE month = %s"
                        cursor.execute(query23, data7)
                        prgf_con = cursor.fetchall()

                        prgf1 = []
                        prgf2 = []

                        for i in range(len(prgf_con)):
                            prgf1 = ''.join(prgf_con[i])
                            prgf2.append(prgf1)
                        prgf_total = 0

                        for i in range(len(prgf2)):
                            prgf_total = int(prgf_total) + int(prgf2[i])                                                

        # =================================================================================================================================

                        query20 = "SELECT csg FROM contribution WHERE month = %s"
                        cursor.execute(query20, data7)
                        csg_con = cursor.fetchall()

                        csg1 = []
                        csg2 = []

                        for i in range(len(csg_con)):
                            csg1 = ''.join(csg_con[i])
                            csg2.append(csg1)
                        csg_total = 0

                        for i in range(len(csg2)):
                            csg_total = int(csg_total) + int(csg2[i])

        # =================================================================================================================================

                        query21 = "SELECT nsf FROM contribution WHERE month = %s"
                        cursor.execute(query21, data7)
                        nsf_con = cursor.fetchall()

                        nsf1 = []
                        nsf2 = []

                        for i in range(len(nsf_con)):
                            nsf1 = ''.join(nsf_con[i])
                            nsf2.append(nsf1)
                        nsf_total = 0

                        for i in range(len(nsf2)):
                            nsf_total = int(nsf_total) + int(nsf2[i])

        # =================================================================================================================================

                        query22 = "SELECT slevy FROM contribution WHERE month = %s"
                        cursor.execute(query22, data7)
                        slevy_con = cursor.fetchall()

                        slevy1 = []
                        slevy2 = []

                        for i in range(len(slevy_con)):
                            slevy1 = ''.join(slevy_con[i])
                            slevy2.append(slevy1)
                        slevy_total = 0

                        for i in range(len(slevy2)):
                            slevy_total = int(slevy_total) + int(slevy2[i])

        # =================================================================================================================================

                        query24 = "SELECT paye FROM contribution WHERE month = %s"
                        cursor.execute(query24, data7)
                        paye_con = cursor.fetchall()

                        paye1 = []
                        paye2 = []

                        for i in range(len(paye_con)):
                            paye1 = ''.join(paye_con[i])
                            paye2.append(paye1)
                        paye_total = 0

                        for i in range(len(paye2)):
                            paye_total = int(paye_total) + int(paye2[i])                    

        # =================================================================================================================================

                        update_contri = """UPDATE contribution
                        SET
                        totalRem = %s,
                        totalecsg = %s,
                        totalelevy = %s,
                        totalensf = %s,
                        totalprgf = %s,
                        totalcsg = %s,
                        totalnsf = %s,
                        totalslevy = %s,
                        totalpaye = %s
                        WHERE 
                        month = %s;
                        """

                        update_contri_data = [bas_total, ecsg_total, elevy_total, ensf_total, prgf_total, csg_total, nsf_total, slevy_total, paye_total, month]

                        cursor.execute(update_contri, update_contri_data)

                        print("Contribution Update Complete")


                        if msg == "Processing Complete":
                            msg = "Processing Complete"
                            # return render_template("process.html", msg = msg)
                        else:
                            msg = "No Employee Available For Process"
                return render_template("process.html", msg = msg)                                
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template("process.html")

@app.route("/EOY", methods=["GET", "POST"])
def eoy():
    if request.method == "POST" and request.form['action'] == 'process':
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            query1_1 = "SELECT EmployeeID FROM employee WHERE Working = 'Yes'"
            cursor.execute(query1_1)
            emp_id = cursor.fetchall()
            emp_id2 = []
            temp = []
            # print(emp_id)

            for i in range(len(emp_id)):
                temp = ''.join(emp_id[i])
                emp_id2.append(temp)
            
            print(emp_id2)

            query2_1 = "SELECT FirstName FROM employee WHERE Working = 'Yes'"
            cursor.execute(query2_1)
            fname_all = cursor.fetchall()
            fname2 = []
            temp2 = []

            # print(fname)

            for i in range(len(fname_all)):
                temp2 = ''.join(fname_all[i])
                fname2.append(temp2)

            print(fname2)

            query3_1 = "SELECT LastName FROM employee WHERE Working = 'Yes'"
            cursor.execute(query3_1)
            lname_all = cursor.fetchall()
            lname2 = []
            temp3 = []

            # print(lname)

            for i in range(len(lname_all)):
                temp3 = ''.join(lname_all[i])
                lname2.append(temp3)
            print(lname2)

            flname1 = []
            flname_all = []

            for i in range(len(emp_id)):
                flname1 = fname2[i] + " " + lname2[i]
                flname_all.append(flname1)

            print(flname_all)

            length = len(flname_all)

# ===========================================================================================================================================================

            eid = request.form["eid"]
            month = "EOY"
            year = date.today().year
            
            eoyBns = request.form["eoy"]
            
            data = [eid]
            # print(month)
            
            print(eid)
            # print(eoyBns)

            id = 12
            mid = id-1
            if mid == 0:
                mid = 12
            
            # print(calendar.month_name[id])
            month2 = calendar.month_name[mid]
            month2 = month2.lower()

            # print(emp_data)
            # print(emp_data[0][0])
            # print(emp_data[0][1])

            car = 0
            tbasic = 0
            fixAllow = 0
            trans = 0
            # edf = 0
            education = 0
            Medicalrel = 0
            medical = 0
            SpeProBns = 0

            data2 = [eid,month2]
            # print(month2)                    
            print("Before Query1")
            query1 = "SELECT FirstName FROM employee WHERE EmployeeID = %s"
            cursor.execute(query1,data)
            fname = cursor.fetchall()
            for i in range(len(fname)):
                fname = ''.join(fname[i])
            print("After Query1")

            query2 = "SELECT LastName FROM employee WHERE EmployeeID = %s"
            cursor.execute(query2,data)
            lname = cursor.fetchall()
            for i in range(len(lname)):
                lname = ''.join(lname[i])

            query8 = "SELECT EDF FROM employee WHERE EmployeeID = %s"
            cursor.execute(query8,data)
            edf = cursor.fetchall()
            for i in range(len(edf)):
                edf = ''.join(edf[i])

            UNQ = month + " " + fname
            data3 = [UNQ]

            query3 = "SELECT ProcBns FROM EOY WHERE UNQ = %s"
            cursor.execute(query3,data3)
            proc = cursor.fetchall()
            print(proc)

            if len(proc) > 0:
                print("In If")
                for i in range(len(proc)):
                    print("In For ")
                    proc = ''.join(proc[i])
            else:
                print("In Else")
                proc = "No"    

# ================================================================================================================================================================================            

            query4 = "SELECT BasicSalary From OriginalData WHERE EmployeeID = %s"
            cursor.execute(query4,data)
            basic_all = cursor.fetchall()
            basic1 = []
            basic2 = []

            for i in range(len(basic_all)):
                basic1 = ''.join(basic_all[i])
                basic2.append(basic1)

            basic_total = 0
            for i in range(len(basic2)):
                basic_total = int(basic_total) + int(basic2[i])

# ================================================================================================================================================================================            

            query5 = "SELECT Overtime From salary WHERE EmployeeID = %s"
            cursor.execute(query5,data)
            overtime_all = cursor.fetchall()
            overtime1 = []
            overtime2 = []

            for i in range(len(overtime_all)):
                overtime1 = ''.join(overtime_all[i])
                overtime2.append(overtime1)

            overtime_total = 0
            for i in range(len(overtime2)):
                overtime_total = int(overtime_total) + int(overtime2[i])

# ================================================================================================================================================================================            

            query6 = "SELECT LeaveRef From salary WHERE EmployeeID = %s"
            cursor.execute(query6,data)
            leave_all = cursor.fetchall()
            leave1 = []
            leave2 = []

            for i in range(len(leave_all)):
                leave1 = ''.join(leave_all[i])
                leave2.append(leave1)

            leave_total = 0
            for i in range(len(leave2)):
                leave_total = int(leave_total) + int(leave2[i])

# ================================================================================================================================================================================            

            query7 = "SELECT OtherAllow From salary WHERE EmployeeID = %s"
            cursor.execute(query7,data)
            other_all = cursor.fetchall()
            other1 = []
            other2 = []

            for i in range(len(other_all)):
                other1 = ''.join(other_all[i])
                other2.append(other1)

            other_total = 0
            for i in range(len(other2)):
                other_total = int(other_total) + int(other2[i])

# ================================================================================================================================================================================            

            query13 = "SELECT Absences From salary WHERE EmployeeID = %s"
            cursor.execute(query13,data)
            ab_all = cursor.fetchall()
            ab1 = []
            ab2 = []

            for i in range(len(ab_all)):
                ab1 = ''.join(ab_all[i])
                ab2.append(ab1)

            ab_total = 0
            for i in range(len(ab2)):
                ab_total = int(ab_total) + int(ab2[i])

# ================================================================================================================================================================================            

            # - (Basic + O/TIME + Local Leave Refund + Other Allowance - Absence ) / 12
            # eoyBns = round((basic_total + overtime_total + leave_total + other_total - ab_total) / 12)
            print(basic_total)
            print(overtime_total)
            print(leave_total)
            print(other_total)
            print(ab_total)
            print(eoyBns)

# ================================================================================================================================================================================            

            query14 = "SELECT salary From employee WHERE EmployeeID = %s "
            cursor.execute(query14,data)
            basic_nov = cursor.fetchall()
            basic_mon = basic_nov[0][0]

            query_month = "SELECT MONTH(hire) AS Month FROM employee WHERE EmployeeID= %s"
            cursor.execute(query_month, data)
            emp_month = cursor.fetchall()
            
            last_mon = emp_month[0][0]

            total_month = 12 - int(last_mon)
            days = total_month * 26

            # eoyBns2 = round((int(basic_mon) /  365) * days)
            eoyBns2 = eoyBns
            
            print("basic_mon ", basic_mon)
            print("days ", days)
            print("eoyBns ", eoyBns2)

# ================================================================================================================================================================================            

            query8 = "SELECT hire FROM employee WHERE EmployeeID = %s"
            cursor.execute(query8,data)
            hire = cursor.fetchall()
            
            hire = hire[0][0] 
            hire = str(hire)
         
            query9 = "SELECT position FROM employee WHERE EmployeeID = %s"
            cursor.execute(query9,data)
            pos = cursor.fetchall()
            for i in range(len(pos)):
                if pos != None:
                    pos = ''.join(pos[i])
                else:
                    pos = " "
            if pos != 0:
                pos = ''.join(map(str,pos))
         
            query10 = "SELECT NICno FROM employee WHERE EmployeeID = %s"
            cursor.execute(query10,data)
            nic = cursor.fetchall()
            # print(nic)
            for i in range(len(nic)):
                if nic[0][0] != None:
                    nic = ''.join(nic[i])
                else:
                    nic = " "
            if nic != 0:
                nic = ''.join(map(str,nic))

            query11 = "SELECT LastName FROM employee WHERE EmployeeID = %s"
            cursor.execute(query11,data)
            ebasic = cursor.fetchall()
            for i in range(len(ebasic)):
                ebasic = ''.join(ebasic[i])

            query12 = "SELECT working FROM employee WHERE EmployeeID = %s"
            cursor.execute(query12,data)
            working = cursor.fetchall()
            for i in range(len(working)):
                working = ''.join(working[i])

            query13 = "SELECT months FROM employee WHERE EmployeeID = %s"
            cursor.execute(query13,data)
            month_count = cursor.fetchall()
            for i in range(len(month_count)):
                month_count = ''.join(month_count[i])

# ============================================================================================================================

            query_day = "SELECT DAY(hire) AS Month FROM employee WHERE EmployeeID= %s"
            cursor.execute(query_day, data)
            emp_day = cursor.fetchall()
            
            last_day = emp_day[0][0]

            query_month = "SELECT MONTH(hire) AS Month FROM employee WHERE EmployeeID= %s"
            cursor.execute(query_month, data)
            emp_month = cursor.fetchall()
            
            last_mon = emp_month[0][0]
            
            query_year = "SELECT YEAR(hire) AS Year FROM employee WHERE EmployeeID= %s"
            cursor.execute(query_year, data)
            emp_year = cursor.fetchall()

            last_year = emp_year[0][0]

            current_year = date.today().year
            bonus_year = current_year - 1

            current_month = date.today().month
            bonus_month = current_month + 1

            # if proc == "No" and last_year < current_year:
            #     if last_mon <= current_month:
            
            prevGross = 0
            piet = 0
            ppaye = 0
            pths = 0
            plevy = 0
            
            flname = lname + " " + fname

            # Values We Don't Get
            ot = 0
            otherAllow = 0
            arrears = 0
            eoy = 0
            leave = 0
            speBns = 0
            discBns = 0
            tax = 0
            ntax = 0
            attBns = 0
            overseas = 0

            loan = 0
            lateness = 0
            otherDed = 0
            ab = 0

            edf = int(edf)
            # basic = int(tbasic) - int(ab)
            
            
            
            basic = int(eoyBns)
            # Calculations
            payable = basic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns
            bonus = speBns + SpeProBns + otherAllow + fixAllow + discBns + attBns

            # For Overseas Amount
            transTax = 0
            ntransTax = 0

            cgross = basic + ot + otherAllow + trans + arrears + eoy + leave + discBns + fixAllow + tax + SpeProBns + attBns + car

            grossTax = basic + ot + transTax +otherAllow + arrears + eoy + leave + discBns + fixAllow  + tax + SpeProBns + attBns + car

            # print("prev Gross " , prevGross)
            # print("Curr Gross " , cgross)
            gross = prevGross + grossTax
            # print("gross" , gross)
            medf = round(int(edf) / int(month_count))
            ciet = round(( int(edf) + int(Medicalrel) + int(education)) / int(month_count))
            
            iet = int(ciet) + int(piet)
            # print("ciet" , ciet)
            # print("piet", piet)
            # print("iet", iet)

            netch = gross - iet

            # print("netch" , netch)
            # netch = 0

            if int(basic) > 50000:
                nps = round(basic * 0.03)
                # cpaye =  round(netch * 0.15)
                enps = round(basic * 0.06)
            else:
                nps = round(basic * 0.015)
                # cpaye = round(netch * 0.1)
                enps = round(basic * 0.03)

            check = int(basic)
            if check < 53846:
                print("In check1")
                cpaye = round(netch* 0.1)
            elif check >= 53846 and check < 75000:
                print("In check2")
                cpaye = round(netch* 0.125)
            else:
                print("In check3")
                cpaye = round(netch* 0.15)

            print("cpaye " , cpaye)
            if cpaye < 0:
                cpaye = 0
            else:
                cpaye = int(cpaye)
            
            print("ppaye " , ppaye)
            if ppaye < 0:
                ppaye = 0
            else:
                ppaye = int(ppaye)

            # print("cpaye", cpaye)
            # print("ppaye", ppaye)
            paye = int(cpaye) - int(ppaye)
            print("paye ", paye)
            if paye < 0:
                paye = 0
            else:
                paye = int(paye)

            nsf = int(basic * 0.01)

            if nsf > 214:
                nsf = 214
            else:
                nsf = int(nsf)

            slevy = 0
            netchar = 0
            
            tths = round(3000000/12)
            ths = int(pths) + int(tths)

            ensf = round(basic * 0.025)
            if ensf > 536:
                ensf = 536
            else:
                ensf = round(ensf)
            
            levy = round(int(basic) * 0.015)
            
            deduction = int(loan) + int(paye) + int(lateness) + int(nps) + int(otherDed) + int(nsf) + int(medical)
            
            net = int(payable) - int(deduction)
            
            # print(slevy)
            
            slevypay = slevy - plevy
            NetPaysheet = int(net) - int(slevypay)
            
            print("slevypay", slevypay)
            otherAllow2 = int(otherAllow) 
            
            tax = int(tax) + int(transTax)
            ntax = int(ntax) + int(ntransTax)
            # Payslip Calculation

            paygross = int(basic) + int(trans) + int(bonus)

            totalDeduction = int(paye) + int(nps) + int(nsf) + int(slevypay)

            netpay = paygross - totalDeduction
            # eprgf = 0
            if basic < 200000:
                eprgf = round((int(basic) + int(bonus)) * 0.035) # + commission
            else:
                eprgf = 0

            print("netpay ", netpay)

            insert_eoy = """INSERT INTO EOY(
                        Employee,
                        BasicSalary,
                        Arrears,
                        Overtime,
                        LeaveRef,
                        EOY,
                        Transport,
                        Overseas,
                        OtherAllow,
                        FixedAllow,
                        Payable,
                        Absences,
                        paye,
                        csg,
                        nsf,
                        Medical,
                        slevy,
                        Lateness,
                        otherDed,
                        Net,
                        month,
                        UNQ,
                        ProcBns,
                        LockBns
                        )
                        VALUES(
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                        );
                        """
            eoy_data = [flname, 0, 0, 0, leave, eoyBns, trans, overseas, otherAllow, 0, payable, 0, paye, nps, nsf, 0, slevypay, 0, otherDed, netpay, "EOY", UNQ, "yes", "no"]
            cursor.execute(insert_eoy,eoy_data)
            print("EOY Query Successful")


            insert_original = """
                    INSERT INTO OriginalData(
                    EmployeeID,
                    EmployeeName,
                    BasicSalary,
                    FixedAllow,
                    OtherDeduction,
                    Overtime,
                    DiscBonus,
                    NSFEmpee,
                    OtherAllow,
                    TaxableAllow,
                    Medical,
                    Transport,
                    overseas,
                    NTaxableAllow,
                    EDF,
                    Arrears,
                    AttendanceBns,
                    EOY,
                    Loan,
                    CarBenefit,
                    LeaveRef,
                    SLevy,
                    SpecialBns,
                    Lateness,
                    EducationRel,                    
                    SpeProBns,
                    NPS,
                    MedicalRel,
                    Payable,
                    Deduction,
                    NetPay,
                    NetPaysheet,
                    CurrentGross,
                    cGrossTax,
                    PrevGross,
                    PrevIET,
                    IET,
                    NetCh,
                    CurrentPAYE,
                    PrevPAYE,
                    PAYE,
                    eCSG,
                    eNSF,
                    eLevy,
                    PRGF,
                    PrevThreshold,
                    Threshold,
                    netchar,
                    CurrentSLevy,
                    PrevSLevy,
                    slevyPay,
                    Absences,
                    Month,
                    Year,
                    UNQ,
                    LockSal
                    )

                    VALUES(
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    );
                    """
            data1 = [eid, flname, basic , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoy, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, "December", year, UNQ, 'No']
            cursor.execute(insert_original, data1)
            print("Insert Original Query Executed")

            insert_salary = """
                    INSERT INTO salary(
                    EmployeeID,
                    EmployeeName,
                    BasicSalary,
                    FixedAllow,
                    OtherDeduction,
                    Overtime,
                    DiscBonus,
                    NSFEmpee,
                    OtherAllow,
                    TaxableAllow,
                    Medical,
                    Transport,
                    overseas,
                    NTaxableAllow,
                    EDF,
                    Arrears,
                    AttendanceBns,
                    EOY,
                    Loan,
                    CarBenefit,
                    LeaveRef,
                    SLevy,
                    SpecialBns,
                    Lateness,
                    EducationRel,                    
                    SpeProBns,
                    NPS,
                    MedicalRel,
                    Payable,
                    Deduction,
                    NetPay,
                    NetPaysheet,
                    CurrentGross,
                    cGrossTax,
                    PrevGross,
                    PrevIET,
                    IET,
                    NetCh,
                    CurrentPAYE,
                    PrevPAYE,
                    PAYE,
                    eCSG,
                    eNSF,
                    eLevy,
                    PRGF,
                    PrevThreshold,
                    Threshold,
                    netchar,
                    CurrentSLevy,
                    PrevSLevy,
                    slevyPay,
                    Absences,
                    Month,
                    Year,
                    UNQ,
                    LockSal,
                    ProcSal
                    )

                    VALUES(
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    );
                    """
            todays_date = date.today()
            year = todays_date.year
            data1 = [eid, flname, basic , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoy, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, "EOY", year, UNQ, 'No', 'Yes']
            cursor.execute(insert_salary, data1)
            print("Update Salary Query Executed")

            insert_payslip = """INSERT INTO payslip(
                            JoinDate,
                            Company,
                            EmpName,
                            Position,
                            NIC,
                            BasicSalary,
                            TravelAlw,
                            Bonus,
                            Gross,
                            PAYE,
                            NPF,
                            NSF,
                            SLevy,
                            Deduction,
                            NetPay,
                            Payable,
                            NetPayAcc,
                            eNPF,
                            eNSF,
                            eLevy,
                            ePRGF,
                            month,
                            UNQ
                            )
                            VALUES(
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                            );
                            """
            data_payslip = [hire, "CARE Ratings (Africa) Private Limitedivate Limited" , flname, pos, nic, basic, trans, bonus, paygross, paye, nps, nsf, slevypay , totalDeduction, netpay,netpay, netpay, enps, ensf, levy, eprgf, "EOY", UNQ ]
            cursor.execute(insert_payslip, data_payslip)
            print("Insert Payslip Query Executed")
            # msg = "Processing Complete"
            
            emolument = int(basic) + int(arrears) + int(overseas) + int(otherAllow) + int(car) + int(ot) + int(eoy) + int(leave) + int(fixAllow) + int(discBns) + int(SpeProBns) + int(speBns) 

            insert_payecsv = """ INSERT INTO payecsv(
                                EmployeeID,
                                LastName,
                                FirstName,
                                Emoluments,
                                PAYE,
                                working,
                                SLevy,
                                EmolumentsNet,
                                month,
                                UNQ
                                )
                                VALUES(
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s
                                );"""
            data4 = [eid, lname, fname, emolument, paye, 'Yes', slevypay, emolument, month, UNQ]
            cursor.execute(insert_payecsv, data4)
            print("Insert PAYE CSV Query Executed")

            msg = "End Of Year Bonus Processing Complete For " + flname + " "
            # elif proc == "No" and last_year == current_year:
            #     prevGross = 0
            #     piet = 0
            #     ppaye = 0
            #     pths = 0
            #     plevy = 0    

            #     flname = lname + " " + fname

            #     # Values We Don't Get
            #     ot = 0
            #     otherAllow = 0
            #     arrears = 0
            #     eoy = 0
            #     leave = 0
            #     speBns = 0
            #     discBns = 0
            #     tax = 0
            #     ntax = 0
            #     attBns = 0
            #     overseas = 0

            #     loan = 0
            #     lateness = 0
            #     otherDed = 0
            #     ab = 0

            #     # basic = int(tbasic) - int(ab)
                
            #     basic = int(eoyBns2)
            #     # Calculations
            #     payable = basic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns
            #     bonus = speBns + SpeProBns + otherAllow + fixAllow + discBns + attBns

            #     # For Overseas Amount
            #     transTax = 0
            #     ntransTax = 0

            #     cgross = basic + ot + otherAllow + trans + arrears + eoy + leave + discBns + fixAllow + tax + SpeProBns + attBns + car

            #     grossTax = basic + ot + transTax +otherAllow + arrears + eoy + leave + discBns + fixAllow  + tax + SpeProBns + attBns + car

            #     # print("prev Gross " , prevGross)
            #     # print("Curr Gross " , cgross)
            #     gross = prevGross + grossTax
            #     # print("gross" , gross)
            #     medf = round(int(edf) / 13)
            #     ciet = round(( int(edf) + int(Medicalrel) + int(education)) / 13)
                
            #     iet = int(ciet) + int(piet)
            #     # print("ciet" , ciet)
            #     # print("piet", piet)
            #     # print("iet", iet)

            #     netch = gross - iet

            #     # print("netch" , netch)
            #     # netch = 0

            #     if int(basic) > 50000:
            #         nps = round(basic * 0.03)
            #         # cpaye =  round(netch * 0.15)
            #         enps = round(basic * 0.06)
            #     else:
            #         nps = round(basic * 0.015)
            #         # cpaye = round(netch * 0.1)
            #         enps = round(basic * 0.03)

            #     check = int(basic)
            #     if check < 53846:
            #         print("In check1")
            #         cpaye = round(netch* 0.1)
            #     elif check >= 53846 and check < 75000:
            #         print("In check2")
            #         cpaye = round(netch* 0.125)
            #     else:
            #         print("In check3")
            #         cpaye = round(netch* 0.15)

            #     print("cpaye " , cpaye)
            #     if cpaye < 0:
            #         cpaye = 0
            #     else:
            #         cpaye = int(cpaye)
                
            #     print("ppaye " , ppaye)
            #     if ppaye < 0:
            #         ppaye = 0
            #     else:
            #         ppaye = int(ppaye)

            #     # print("cpaye", cpaye)
            #     # print("ppaye", ppaye)
            #     paye = int(cpaye) - int(ppaye)
            #     print("paye ", paye)
            #     if paye < 0:
            #         paye = 0
            #     else:
            #         paye = int(paye)

            #     nsf = int(basic * 0.01)

            #     if nsf > 214:
            #         nsf = 214
            #     else:
            #         nsf = int(nsf)

            #     slevy = 0
            #     netchar = 0
                
            #     tths = round(3000000/12)
            #     ths = int(pths) + int(tths)

            #     ensf = round(basic * 0.025)
            #     if ensf > 536:
            #         ensf = 536
            #     else:
            #         ensf = round(ensf)
                
            #     levy = round(int(basic) * 0.015)
                
            #     deduction = int(loan) + int(paye) + int(lateness) + int(nps) + int(otherDed) + int(nsf) + int(medical)
                
            #     net = int(payable) - int(deduction)
                
            #     # print(slevy)
                
                
            #     slevypay = slevy - plevy
            #     NetPaysheet = int(net) - int(slevypay)
                
            #     print("slevypay", slevypay)
            #     otherAllow2 = int(otherAllow) 
                
            #     tax = int(tax) + int(transTax)
            #     ntax = int(ntax) + int(ntransTax)
            #     # Payslip Calculation

            #     paygross = int(basic) + int(trans) + int(bonus)

            #     totalDeduction = int(paye) + int(nps) + int(nsf) + int(slevypay)

            #     netpay = paygross - totalDeduction
            #     # eprgf = 0
            #     if basic < 200000:
            #         eprgf = round((int(basic) + int(bonus)) * 0.035) # + commission
            #     else:
            #         eprgf = 0

            #     print("netpay ", netpay)

            #     insert_eoy = """INSERT INTO EOY(
            #                 Employee,
            #                 BasicSalary,
            #                 Arrears,
            #                 Overtime,
            #                 LeaveRef,
            #                 EOY,
            #                 Transport,
            #                 Overseas,
            #                 OtherAllow,
            #                 FixedAllow,
            #                 Payable,
            #                 Absences,
            #                 paye,
            #                 csg,
            #                 nsf,
            #                 Medical,
            #                 slevy,
            #                 Lateness,
            #                 otherDed,
            #                 Net,
            #                 month,
            #                 UNQ,
            #                 ProcBns,
            #                 LockBns
            #                 )
            #                 VALUES(
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s,
            #                 %s
            #                 );
            #                 """
            #     eoy_data = [flname, 0, 0, 0, leave, eoyBns2, trans, overseas, otherAllow, 0, payable, 0, paye, nps, nsf, 0, slevypay, 0, otherDed, netpay, "EOY", UNQ, "yes", "no"]
            #     cursor.execute(insert_eoy,eoy_data)
            #     print("EOY Query Successful")

            #     insert_original = """
            #             INSERT INTO OriginalData(
            #             EmployeeID,
            #             EmployeeName,
            #             BasicSalary,
            #             FixedAllow,
            #             OtherDeduction,
            #             Overtime,
            #             DiscBonus,
            #             NSFEmpee,
            #             OtherAllow,
            #             TaxableAllow,
            #             Medical,
            #             Transport,
            #             overseas,
            #             NTaxableAllow,
            #             EDF,
            #             Arrears,
            #             AttendanceBns,
            #             EOY,
            #             Loan,
            #             CarBenefit,
            #             LeaveRef,
            #             SLevy,
            #             SpecialBns,
            #             Lateness,
            #             EducationRel,                    
            #             SpeProBns,
            #             NPS,
            #             MedicalRel,
            #             Payable,
            #             Deduction,
            #             NetPay,
            #             NetPaysheet,
            #             CurrentGross,
            #             cGrossTax,
            #             PrevGross,
            #             PrevIET,
            #             IET,
            #             NetCh,
            #             CurrentPAYE,
            #             PrevPAYE,
            #             PAYE,
            #             eCSG,
            #             eNSF,
            #             eLevy,
            #             PRGF,
            #             PrevThreshold,
            #             Threshold,
            #             netchar,
            #             CurrentSLevy,
            #             PrevSLevy,
            #             slevyPay,
            #             Absences,
            #             Month,
            #             Year,
            #             UNQ,
            #             LockSal
            #             )

            #             VALUES(
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s
            #             );
            #             """
            #     data1 = [eid, flname, basic , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoy, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, "December", year, UNQ, 'No']
            #     cursor.execute(insert_original, data1)
            #     print("Insert Original Query Executed")

            #     insert_salary = """
            #             INSERT INTO salary(
            #             EmployeeID,
            #             EmployeeName,
            #             BasicSalary,
            #             FixedAllow,
            #             OtherDeduction,
            #             Overtime,
            #             DiscBonus,
            #             NSFEmpee,
            #             OtherAllow,
            #             TaxableAllow,
            #             Medical,
            #             Transport,
            #             overseas,
            #             NTaxableAllow,
            #             EDF,
            #             Arrears,
            #             AttendanceBns,
            #             EOY,
            #             Loan,
            #             CarBenefit,
            #             LeaveRef,
            #             SLevy,
            #             SpecialBns,
            #             Lateness,
            #             EducationRel,                    
            #             SpeProBns,
            #             NPS,
            #             MedicalRel,
            #             Payable,
            #             Deduction,
            #             NetPay,
            #             NetPaysheet,
            #             CurrentGross,
            #             cGrossTax,
            #             PrevGross,
            #             PrevIET,
            #             IET,
            #             NetCh,
            #             CurrentPAYE,
            #             PrevPAYE,
            #             PAYE,
            #             eCSG,
            #             eNSF,
            #             eLevy,
            #             PRGF,
            #             PrevThreshold,
            #             Threshold,
            #             netchar,
            #             CurrentSLevy,
            #             PrevSLevy,
            #             slevyPay,
            #             Absences,
            #             Month,
            #             Year,
            #             UNQ,
            #             LockSal,
            #             ProcSal
            #             )

            #             VALUES(
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s,
            #             %s
            #             );
            #             """
            #     todays_date = date.today()
            #     year = todays_date.year
            #     data1 = [eid, flname, basic , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoyBns2, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, "EOY", year, UNQ, 'No', 'Yes']
            #     cursor.execute(insert_salary, data1)
            #     print("Update Salary Query Executed")

            #     insert_payslip = """INSERT INTO payslip(
            #                     JoinDate,
            #                     Company,
            #                     EmpName,
            #                     Position,
            #                     NIC,
            #                     BasicSalary,
            #                     TravelAlw,
            #                     Bonus,
            #                     Gross,
            #                     PAYE,
            #                     NPF,
            #                     NSF,
            #                     SLevy,
            #                     Deduction,
            #                     NetPay,
            #                     Payable,
            #                     NetPayAcc,
            #                     eNPF,
            #                     eNSF,
            #                     eLevy,
            #                     ePRGF,
            #                     month,
            #                     UNQ
            #                     )
            #                     VALUES(
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s,
            #                     %s
            #                     );
            #                     """
            #     data_payslip = [hire, "CARE Ratings (Africa) Private Limited" , flname, pos, nic, basic, trans, bonus, paygross, paye, nps, nsf, slevypay , totalDeduction, netpay,netpay, netpay, enps, ensf, levy, eprgf, "EOY", UNQ ]
            #     cursor.execute(insert_payslip, data_payslip)
            #     print("Insert Payslip Query Executed")
            #     # msg = "Processing Complete"
                
            #     emolument = int(basic) + int(arrears) + int(overseas) + int(otherAllow) + int(car) + int(ot) + int(eoy) + int(leave) + int(fixAllow) + int(discBns) + int(SpeProBns) + int(speBns) 

            #     insert_payecsv = """ INSERT INTO payecsv(
            #                         EmployeeID,
            #                         LastName,
            #                         FirstName,
            #                         Emoluments,
            #                         PAYE,
            #                         working,
            #                         SLevy,
            #                         EmolumentsNet,
            #                         month,
            #                         UNQ
            #                         )
            #                         VALUES(
            #                             %s,
            #                             %s,
            #                             %s,
            #                             %s,
            #                             %s,
            #                             %s,
            #                             %s,
            #                             %s,
            #                             %s,
            #                             %s
            #                         );"""
            #     data4 = [eid, lname, fname, emolument, paye, 'Yes', slevypay, emolument, month, UNQ]
            #     cursor.execute(insert_payecsv, data4)
            #     print("Insert PAYE CSV Query Executed")
            #     msg = "End Of Year Bonus (Prorata basic) Process Complete For " + flname + " "
            # else:
            #     msg = "Bonus Already Processed."

            # print(msg)
            return render_template("eoy.html", msg=msg, eid = emp_id2, name=flname_all, length = length)
        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    elif request.method == "POST" and request.form['action'] == 'reprocess':
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            query1_1 = "SELECT EmployeeID FROM employee"
            cursor.execute(query1_1)
            emp_id = cursor.fetchall()
            emp_id2 = []
            temp = []
            # print(emp_id)

            for i in range(len(emp_id)):
                temp = ''.join(emp_id[i])
                emp_id2.append(temp)
            
            # print(emp_id2)

            query2_1 = "SELECT FirstName FROM employee"
            cursor.execute(query2_1)
            fname_all = cursor.fetchall()
            fname2 = []
            temp2 = []

            # print(fname)

            for i in range(len(fname_all)):
                temp2 = ''.join(fname_all[i])
                fname2.append(temp2)

            # print(fname2)

            query3_1 = "SELECT LastName FROM employee"
            cursor.execute(query3_1)
            lname_all = cursor.fetchall()
            lname2 = []
            temp3 = []

            # print(lname)

            for i in range(len(lname_all)):
                temp3 = ''.join(lname_all[i])
                lname2.append(temp3)
            # print(lname2)

            flname1 = []
            flname_all = []

            for i in range(len(emp_id)):
                flname1 = fname2[i] + " " + lname2[i]
                flname_all.append(flname1)

            # print(flname_all)

            length = len(flname_all)
# ===========================================================================================================================================================

            eid = request.form["eid"]
            eoyBns = request.form["eoy"]
            month = "EOY"
            year = date.today().year
            
            data = [eid]
            # print(month)

            id = 12
            mid = id-1
            if mid == 0:
                mid = 12
            
            # print(calendar.month_name[id])
            month2 = calendar.month_name[mid]
            month2 = month2.lower()

            # print(emp_data)
            # print(emp_data[0][0])
            # print(emp_data[0][1])

            car = 0
            tbasic = 0
            fixAllow = 0
            trans = 0
            edf = 0
            education = 0
            Medicalrel = 0
            medical = 0
            SpeProBns = 0

            data2 = [eid,month2]
            # print(month2)                    

            query1 = "SELECT FirstName FROM employee WHERE EmployeeID = %s"
            cursor.execute(query1,data)
            fname = cursor.fetchall()
            for i in range(len(fname)):
                fname = ''.join(fname[i])

            query2 = "SELECT LastName FROM employee WHERE EmployeeID = %s"
            cursor.execute(query2,data)
            lname = cursor.fetchall()
            for i in range(len(lname)):
                lname = ''.join(lname[i])

            UNQ = month + " " + fname
            data3 = [UNQ]

            print("UNQ ", UNQ)

            query3 = "SELECT ProcBns FROM EOY WHERE UNQ = %s"
            cursor.execute(query3,data3)
            proc = cursor.fetchall()
            print("proc ", proc)

# ================================================================================================================================================================================            

            query4 = "SELECT BasicSalary From salary WHERE EmployeeID = %s"
            cursor.execute(query4,data)
            basic_all = cursor.fetchall()
            basic1 = []
            basic2 = []

            for i in range(len(basic_all)):
                basic1 = ''.join(basic_all[i])
                basic2.append(basic1)

            basic_total = 0
            for i in range(len(basic2)):
                basic_total = int(basic_total) + int(basic2[i])

# ================================================================================================================================================================================            

            query5 = "SELECT Overtime From salary WHERE EmployeeID = %s"
            cursor.execute(query5,data)
            overtime_all = cursor.fetchall()
            overtime1 = []
            overtime2 = []

            for i in range(len(overtime_all)):
                overtime1 = ''.join(overtime_all[i])
                overtime2.append(overtime1)

            overtime_total = 0
            for i in range(len(overtime2)):
                overtime_total = int(overtime_total) + int(overtime2[i])

# ================================================================================================================================================================================            

            query6 = "SELECT LeaveRef From salary WHERE EmployeeID = %s"
            cursor.execute(query6,data)
            leave_all = cursor.fetchall()
            leave1 = []
            leave2 = []

            for i in range(len(leave_all)):
                leave1 = ''.join(leave_all[i])
                leave2.append(leave1)

            leave_total = 0
            for i in range(len(leave2)):
                leave_total = int(leave_total) + int(leave2[i])

# ================================================================================================================================================================================            

            query7 = "SELECT OtherAllow From salary WHERE EmployeeID = %s"
            cursor.execute(query7,data)
            other_all = cursor.fetchall()
            other1 = []
            other2 = []

            for i in range(len(other_all)):
                other1 = ''.join(other_all[i])
                other2.append(other1)

            other_total = 0
            for i in range(len(other2)):
                other_total = int(other_total) + int(other2[i])

# ================================================================================================================================================================================            

            query14 = "SELECT Absences From salary WHERE EmployeeID = %s"
            cursor.execute(query14,data)
            ab_all = cursor.fetchall()
            ab1 = []
            ab2 = []

            for i in range(len(ab_all)):
                ab1 = ''.join(ab_all[i])
                ab2.append(ab1)

            ab_total = 0
            for i in range(len(ab2)):
                ab_total = int(ab_total) + int(ab2[i])

# ================================================================================================================================================================================            

            # - (Basic + O/TIME + Local Leave Refund + Other Allowance - Absence ) / 12
            # eoyBns = round((basic_total + overtime_total + leave_total + other_total - ab_total) / 12)
            print(basic_total)
            print(overtime_total)
            print(leave_total)
            print(other_total)
            print(ab_total)
            print(eoyBns)

# ================================================================================================================================================================================            
            
            query15 = "SELECT salary From employee WHERE EmployeeID = %s "
            cursor.execute(query15,data)
            basic_nov = cursor.fetchall()
            basic_mon = basic_nov[0][0]

            query_month = "SELECT MONTH(hire) AS Month FROM employee WHERE EmployeeID= %s"
            cursor.execute(query_month, data)
            emp_month = cursor.fetchall()
            
            last_mon = emp_month[0][0]

            total_month = 12 - int(last_mon)
            days = total_month * 26

            # eoyBns2 = round((int(basic_mon) /  365) * days)
            eoyBns2 = eoyBns
            
            print("basic_mon ", basic_mon)
            print("days ", days)
            print("eoyBns ", eoyBns2)

# ================================================================================================================================================================================            
            
            # if len(proc) > 0:
            #     print("In If")
            #     for i in range(len(proc)):
            #         print("In For ")
            #         proc = ''.join(proc[i])
            # else:
            #     print("In Else")
            #     proc = "No"    
            
            query8 = "SELECT hire FROM employee WHERE EmployeeID = %s"
            cursor.execute(query8,data)
            hire = cursor.fetchall()
            
            hire = hire[0][0] 
            hire = str(hire)
         
            query9 = "SELECT position FROM employee WHERE EmployeeID = %s"
            cursor.execute(query9,data)
            pos = cursor.fetchall()
            for i in range(len(pos)):
                if pos != None:
                    pos = ''.join(pos[i])
                else:
                    pos = " "
            if pos != 0:
                pos = ''.join(map(str,pos))

            print("proc ", proc )
         
            query10 = "SELECT NICno FROM employee WHERE EmployeeID = %s"
            cursor.execute(query10,data)
            nic = cursor.fetchall()
            # print(nic)
            for i in range(len(nic)):
                if nic[0][0] != None:
                    nic = ''.join(nic[i])
                else:
                    nic = " "
            if nic != 0:
                nic = ''.join(map(str,nic))

            query11 = "SELECT LastName FROM employee WHERE EmployeeID = %s"
            cursor.execute(query11,data)
            ebasic = cursor.fetchall()
            for i in range(len(ebasic)):
                ebasic = ''.join(ebasic[i])

            query12 = "SELECT working FROM employee WHERE EmployeeID = %s"
            cursor.execute(query12,data)
            working = cursor.fetchall()
            for i in range(len(working)):
                working = ''.join(working[i])

            query13 = "SELECT months FROM employee WHERE EmployeeID = %s"
            cursor.execute(query13,data)
            month_count = cursor.fetchall()
            for i in range(len(month_count)):
                month_count = ''.join(month_count[i])

# ============================================================================================================================

            query_day = "SELECT DAY(hire) AS Month FROM employee WHERE EmployeeID= %s"
            cursor.execute(query_day, data)
            emp_day = cursor.fetchall()
            
            last_day = emp_day[0][0]

            query_month = "SELECT MONTH(hire) AS Month FROM employee WHERE EmployeeID= %s"
            cursor.execute(query_month, data)
            emp_month = cursor.fetchall()
            
            last_mon = emp_month[0][0]
            
            query_year = "SELECT YEAR(hire) AS Year FROM employee WHERE EmployeeID= %s"
            cursor.execute(query_year, data)
            emp_year = cursor.fetchall()

            last_year = emp_year[0][0]

            current_year = date.today().year
            bonus_year = current_year - 1

            current_month = date.today().month
            bonus_month = current_month + 1
            
            if proc != [] and last_year < current_year:
                if last_mon <= current_month:
                    print("In If Proc")

                    prevGross = 0
                    piet = 0
                    ppaye = 0
                    pths = 0
                    plevy = 0    
                    
                    flname = lname + " " + fname

                    # Values We Don't Get
                    ot = 0
                    otherAllow = 0
                    arrears = 0
                    eoy = 0
                    leave = 0
                    speBns = 0
                    discBns = 0
                    tax = 0
                    ntax = 0
                    attBns = 0
                    overseas = 0

                    loan = 0
                    lateness = 0
                    otherDed = 0
                    ab = 0

                    # basic = int(tbasic) - int(ab)
                    basic = int(eoyBns)
                    # Calculations
                    payable = basic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns
                    bonus = speBns + SpeProBns + otherAllow + fixAllow + discBns + attBns

                    # For Overseas Amount
                    transTax = 0
                    ntransTax = 0

                    cgross = basic + ot + otherAllow + trans + arrears + eoy + leave + discBns + fixAllow + tax + SpeProBns + attBns + car

                    grossTax = basic + ot + transTax +otherAllow + arrears + eoy + leave + discBns + fixAllow  + tax + SpeProBns + attBns + car

                    # print("prev Gross " , prevGross)
                    # print("Curr Gross " , cgross)
                    gross = prevGross + grossTax
                    # print("gross" , gross)
                    medf = round(int(edf) / int(month_count))
                    ciet = round(( int(edf) + int(Medicalrel) + int(education)) / int(month_count))
                    
                    iet = int(ciet) + int(piet)
                    # print("ciet" , ciet)
                    # print("piet", piet)
                    # print("iet", iet)

                    netch = gross - iet

                    # print("netch" , netch)
                    # netch = 0

                    if int(basic) > 50000:
                        nps = round(basic * 0.03)
                        # cpaye =  round(netch * 0.15)
                        enps = round(basic * 0.06)
                    else:
                        nps = round(basic * 0.015)
                        # cpaye = round(netch * 0.1)
                        enps = round(basic * 0.03)

                    check = int(basic)
                    if check < 53846:
                        print("In check1")
                        cpaye = round(netch* 0.1)
                    elif check >= 53846 and check < 75000:
                        print("In check2")
                        cpaye = round(netch* 0.125)
                    else:
                        print("In check3")
                        cpaye = round(netch* 0.15)

                    print("cpaye " , cpaye)
                    if cpaye < 0:
                        cpaye = 0
                    else:
                        cpaye = int(cpaye)
                    
                    print("ppaye " , ppaye)
                    if ppaye < 0:
                        ppaye = 0
                    else:
                        ppaye = int(ppaye)

                    # print("cpaye", cpaye)
                    # print("ppaye", ppaye)
                    paye = int(cpaye) - int(ppaye)
                    print("paye ", paye)
                    if paye < 0:
                        paye = 0
                    else:
                        paye = int(paye)

                    nsf = int(basic * 0.01)

                    if nsf > 214:
                        nsf = 214
                    else:
                        nsf = int(nsf)

                    slevy = 0
                    netchar = 0
                    
                    tths = round(3000000/12)
                    ths = int(pths) + int(tths)

                    ensf = round(basic * 0.025)
                    if ensf > 536:
                        ensf = 536
                    else:
                        ensf = round(ensf)
                    
                    levy = round(int(basic) * 0.015)
                    
                    deduction = int(loan) + int(paye) + int(lateness) + int(nps) + int(otherDed) + int(nsf) + int(medical)
                    
                    net = int(payable) - int(deduction)
                    
                    # print(slevy)
                    
                    
                    slevypay = slevy - plevy
                    NetPaysheet = int(net) - int(slevypay)
                    
                    print("slevypay", slevypay)
                    otherAllow2 = int(otherAllow) 
                    
                    tax = int(tax) + int(transTax)
                    ntax = int(ntax) + int(ntransTax)
                    # Payslip Calculation

                    paygross = int(basic) + int(trans) + int(bonus)

                    totalDeduction = int(paye) + int(nps) + int(nsf) + int(slevypay)

                    netpay = paygross - totalDeduction
                    # eprgf = 0
                    if basic < 200000:
                        eprgf = round((int(basic) + int(bonus)) * 0.035) # + commission
                    else:
                        eprgf = 0

                    print("netpay ", netpay)

                    update_eoy = """UPDATE EOY
                                SET
                                Employee = %s,
                                BasicSalary = %s,
                                Arrears = %s,
                                Overtime = %s,
                                LeaveRef = %s,
                                EOY = %s,
                                Transport = %s,
                                Overseas = %s,
                                OtherAllow = %s,
                                FixedAllow = %s,
                                Payable = %s,
                                Absences = %s,
                                paye = %s,
                                csg = %s,
                                nsf = %s,
                                Medical = %s,
                                slevy = %s,
                                Lateness = %s,
                                otherDed = %s,
                                Net = %s,
                                month = %s
                                WHERE
                                UNQ = %s;
                                """

                    print("EOY ", eoyBns2)
                    eoy_data = [flname, 0, 0, 0, leave, eoyBns, trans, overseas, otherAllow, 0, payable, 0, paye, nps, nsf, 0, slevypay, 0, otherDed, netpay, "EOY", UNQ]
                    cursor.execute(update_eoy,eoy_data)
                    print("UPDATE EOY Query Successful")


                    update_original = """UPDATE OriginalData
                                        SET
                                        EmployeeID = %s,
                                        EmployeeName = %s,
                                        BasicSalary = %s,
                                        FixedAllow = %s,
                                        OtherDeduction = %s,
                                        Overtime = %s,
                                        DiscBonus = %s,
                                        NSFEmpee = %s,
                                        OtherAllow = %s,
                                        TaxableAllow = %s,
                                        Medical = %s,
                                        Transport = %s,
                                        overseas = %s,
                                        NTaxableAllow = %s,
                                        EDF = %s,
                                        Arrears = %s,
                                        AttendanceBns = %s,
                                        EOY = %s,
                                        Loan = %s,
                                        CarBenefit = %s,
                                        LeaveRef = %s,
                                        SLevy = %s,
                                        SpecialBns = %s,
                                        Lateness = %s,
                                        EducationRel = %s,
                                        SpeProBns = %s,
                                        NPS = %s,
                                        MedicalRel = %s,
                                        Payable = %s,
                                        Deduction = %s,
                                        NetPay = %s,
                                        NetPaysheet = %s,
                                        CurrentGross = %s,
                                        cGrossTax = %s,
                                        PrevGross = %s,
                                        PrevIET = %s,
                                        IET = %s,
                                        NetCh = %s,
                                        CurrentPAYE = %s,
                                        PrevPAYE = %s,
                                        PAYE = %s,
                                        eCSG = %s,
                                        eNSF = %s,
                                        eLevy = %s,
                                        PRGF = %s,
                                        PrevThreshold = %s,
                                        Threshold = %s,
                                        netchar = %s,
                                        CurrentSLevy = %s,
                                        PrevSLevy = %s,
                                        slevyPay = %s,
                                        Absences = %s
                                        WHERE 
                                        UNQ = %s;
                                        """
                    data1 = [eid, flname, 0 , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoyBns2, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, UNQ]
                    cursor.execute(update_original, data1)
                    print("Update Original Query Executed")

                    update_salary = """UPDATE salary
                                        SET
                                        EmployeeID = %s,
                                        EmployeeName = %s,
                                        BasicSalary = %s,
                                        FixedAllow = %s,
                                        OtherDeduction = %s,
                                        Overtime = %s,
                                        DiscBonus = %s,
                                        NSFEmpee = %s,
                                        OtherAllow = %s,
                                        TaxableAllow = %s,
                                        Medical = %s,
                                        Transport = %s,
                                        overseas = %s,
                                        NTaxableAllow = %s,
                                        EDF = %s,
                                        Arrears = %s,
                                        AttendanceBns = %s,
                                        EOY = %s,
                                        Loan = %s,
                                        CarBenefit = %s,
                                        LeaveRef = %s,
                                        SLevy = %s,
                                        SpecialBns = %s,
                                        Lateness = %s,
                                        EducationRel = %s,
                                        SpeProBns = %s,
                                        NPS = %s,
                                        MedicalRel = %s,
                                        Payable = %s,
                                        Deduction = %s,
                                        NetPay = %s,
                                        NetPaysheet = %s,
                                        CurrentGross = %s,
                                        cGrossTax = %s,
                                        PrevGross = %s,
                                        PrevIET = %s,
                                        IET = %s,
                                        NetCh = %s,
                                        CurrentPAYE = %s,
                                        PrevPAYE = %s,
                                        PAYE = %s,
                                        eCSG = %s,
                                        eNSF = %s,
                                        eLevy = %s,
                                        PRGF = %s,
                                        PrevThreshold = %s,
                                        Threshold = %s,
                                        netchar = %s,
                                        CurrentSLevy = %s,
                                        PrevSLevy = %s,
                                        slevyPay = %s,
                                        Absences = %s
                                        WHERE
                                        UNQ = %s
                                        """
                        
                    data2 = [eid, flname, 0 , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoyBns2, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, UNQ]
                    cursor.execute(update_salary, data2)
                    print("Update Salary Query Executed")

                    update_payslip = """UPDATE payslip
                                SET
                                EmpName = %s,
                                Position = %s,
                                NIC = %s,
                                BasicSalary = %s,
                                TravelAlw = %s,
                                Bonus = %s,
                                Gross = %s,
                                PAYE = %s,
                                NPF = %s,
                                NSF = %s,
                                SLevy = %s,
                                Deduction = %s,
                                NetPay = %s,
                                Payable = %s,
                                NetPayAcc = %s,
                                eNPF = %s,
                                eNSF = %s,
                                eLevy = %s,
                                ePRGF = %s,
                                month = %s
                                WHERE
                                UNQ = %s;
                                """
                    data_payslip = [flname, pos, nic, 0, trans, bonus, paygross, paye, nps, nsf, slevypay, totalDeduction, netpay, netpay, netpay,  enps, ensf, levy, eprgf, "EOY", UNQ]
                    cursor.execute(update_payslip, data_payslip)
                    print("Update Payslip Query Executed")
                    # msg = "Processing Complete"
                    
                    emolument = int(basic) + int(arrears) + int(overseas) + int(otherAllow) + int(car) + int(ot) + int(eoy) + int(leave) + int(fixAllow) + int(discBns) + int(SpeProBns) + int(speBns) 

                    update_payecsv = """UPDATE payecsv
                                        SET
                                        EmployeeID = %s,
                                        LastName = %s,
                                        FirstName = %s,
                                        Emoluments = %s,
                                        PAYE = %s,
                                        SLevy = %s,
                                        EmolumentsNet = %s
                                        WHERE
                                        UNQ = %s;
                                        """

                    data4 = [eid, lname, fname, emolument, paye, slevypay, emolument, UNQ]
                    cursor.execute(update_payecsv, data4)
                    print("Update PAYE CSV Query Executed")

                    msg = "End Of Year Bonus Re-Processing Complete For " + flname + " "
            elif proc != [] and last_year == current_year:
                prevGross = 0
                piet = 0
                ppaye = 0
                pths = 0
                plevy = 0    
                
                flname = lname + " " + fname

                # Values We Don't Get
                ot = 0
                otherAllow = 0
                arrears = 0
                eoy = 0
                leave = 0
                speBns = 0
                discBns = 0
                tax = 0
                ntax = 0
                attBns = 0
                overseas = 0

                loan = 0
                lateness = 0
                otherDed = 0
                ab = 0

                # basic = int(tbasic) - int(ab)
                basic = int(eoyBns2)
                # Calculations
                payable = basic + ot + otherAllow + trans + arrears + eoy + leave + speBns + SpeProBns + fixAllow + discBns + overseas + attBns
                bonus = speBns + SpeProBns + otherAllow + fixAllow + discBns + attBns

                # For Overseas Amount
                transTax = 0
                ntransTax = 0

                cgross = basic + ot + otherAllow + trans + arrears + eoy + leave + discBns + fixAllow + tax + SpeProBns + attBns + car

                grossTax = basic + ot + transTax +otherAllow + arrears + eoy + leave + discBns + fixAllow  + tax + SpeProBns + attBns + car

                # print("prev Gross " , prevGross)
                # print("Curr Gross " , cgross)
                gross = prevGross + grossTax
                # print("gross" , gross)
                medf = round(int(edf) / int(month_count))
                ciet = round(( int(edf) + int(Medicalrel) + int(education)) / int(month_count))
                
                iet = int(ciet) + int(piet)
                # print("ciet" , ciet)
                # print("piet", piet)
                # print("iet", iet)

                netch = gross - iet

                # print("netch" , netch)
                # netch = 0

                if int(basic) > 50000:
                    nps = round(basic * 0.03)
                    # cpaye =  round(netch * 0.15)
                    enps = round(basic * 0.06)
                else:
                    nps = round(basic * 0.015)
                    # cpaye = round(netch * 0.1)
                    enps = round(basic * 0.03)

                check = int(basic)
                if check < 53846:
                    print("In check1")
                    cpaye = round(netch* 0.1)
                elif check >= 53846 and check < 75000:
                    print("In check2")
                    cpaye = round(netch* 0.125)
                else:
                    print("In check3")
                    cpaye = round(netch* 0.15)

                print("cpaye " , cpaye)
                if cpaye < 0:
                    cpaye = 0
                else:
                    cpaye = int(cpaye)
                
                print("ppaye " , ppaye)
                if ppaye < 0:
                    ppaye = 0
                else:
                    ppaye = int(ppaye)

                # print("cpaye", cpaye)
                # print("ppaye", ppaye)
                paye = int(cpaye) - int(ppaye)
                print("paye ", paye)
                if paye < 0:
                    paye = 0
                else:
                    paye = int(paye)

                nsf = int(basic * 0.01)

                if nsf > 214:
                    nsf = 214
                else:
                    nsf = int(nsf)

                slevy = 0
                netchar = 0
                
                tths = round(3000000/12)
                ths = int(pths) + int(tths)

                ensf = round(basic * 0.025)
                if ensf > 536:
                    ensf = 536
                else:
                    ensf = round(ensf)
                
                levy = round(int(basic) * 0.015)
                
                deduction = int(loan) + int(paye) + int(lateness) + int(nps) + int(otherDed) + int(nsf) + int(medical)
                
                net = int(payable) - int(deduction)
                
                # print(slevy)
                
                
                slevypay = slevy - plevy
                NetPaysheet = int(net) - int(slevypay)
                
                print("slevypay", slevypay)
                otherAllow2 = int(otherAllow) 
                
                tax = int(tax) + int(transTax)
                ntax = int(ntax) + int(ntransTax)
                # Payslip Calculation

                paygross = int(basic) + int(trans) + int(bonus)

                totalDeduction = int(paye) + int(nps) + int(nsf) + int(slevypay)

                netpay = paygross - totalDeduction
                # eprgf = 0
                if basic < 200000:
                    eprgf = round((int(basic) + int(bonus)) * 0.035) # + commission
                else:
                    eprgf = 0

                print("netpay ", netpay)

                update_eoy = """UPDATE EOY
                            SET
                            Employee = %s,
                            BasicSalary = %s,
                            Arrears = %s,
                            Overtime = %s,
                            LeaveRef = %s,
                            EOY = %s,
                            Transport = %s,
                            Overseas = %s,
                            OtherAllow = %s,
                            FixedAllow = %s,
                            Payable = %s,
                            Absences = %s,
                            paye = %s,
                            csg = %s,
                            nsf = %s,
                            Medical = %s,
                            slevy = %s,
                            Lateness = %s,
                            otherDed = %s,
                            Net = %s,
                            month = %s
                            WHERE
                            UNQ = %s;
                            """

                print("EOY ", eoyBns)
                eoy_data = [flname, 0, 0, 0, leave, eoyBns2, trans, overseas, otherAllow, 0, payable, 0, paye, nps, nsf, 0, slevypay, 0, otherDed, netpay, "EOY", UNQ]
                cursor.execute(update_eoy,eoy_data)
                print("UPDATE EOY Query Successful")

                update_original = """UPDATE OriginalData
                                    SET
                                    EmployeeID = %s,
                                    EmployeeName = %s,
                                    BasicSalary = %s,
                                    FixedAllow = %s,
                                    OtherDeduction = %s,
                                    Overtime = %s,
                                    DiscBonus = %s,
                                    NSFEmpee = %s,
                                    OtherAllow = %s,
                                    TaxableAllow = %s,
                                    Medical = %s,
                                    Transport = %s,
                                    overseas = %s,
                                    NTaxableAllow = %s,
                                    EDF = %s,
                                    Arrears = %s,
                                    AttendanceBns = %s,
                                    EOY = %s,
                                    Loan = %s,
                                    CarBenefit = %s,
                                    LeaveRef = %s,
                                    SLevy = %s,
                                    SpecialBns = %s,
                                    Lateness = %s,
                                    EducationRel = %s,
                                    SpeProBns = %s,
                                    NPS = %s,
                                    MedicalRel = %s,
                                    Payable = %s,
                                    Deduction = %s,
                                    NetPay = %s,
                                    NetPaysheet = %s,
                                    CurrentGross = %s,
                                    cGrossTax = %s,
                                    PrevGross = %s,
                                    PrevIET = %s,
                                    IET = %s,
                                    NetCh = %s,
                                    CurrentPAYE = %s,
                                    PrevPAYE = %s,
                                    PAYE = %s,
                                    eCSG = %s,
                                    eNSF = %s,
                                    eLevy = %s,
                                    PRGF = %s,
                                    PrevThreshold = %s,
                                    Threshold = %s,
                                    netchar = %s,
                                    CurrentSLevy = %s,
                                    PrevSLevy = %s,
                                    slevyPay = %s,
                                    Absences = %s
                                    WHERE 
                                    UNQ = %s;
                                    """
                data1 = [eid, flname, 0 , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoyBns2, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, UNQ]
                cursor.execute(update_original, data1)
                print("Update Original Query Executed")

                update_salary = """UPDATE salary
                                    SET
                                    EmployeeID = %s,
                                    EmployeeName = %s,
                                    BasicSalary = %s,
                                    FixedAllow = %s,
                                    OtherDeduction = %s,
                                    Overtime = %s,
                                    DiscBonus = %s,
                                    NSFEmpee = %s,
                                    OtherAllow = %s,
                                    TaxableAllow = %s,
                                    Medical = %s,
                                    Transport = %s,
                                    overseas = %s,
                                    NTaxableAllow = %s,
                                    EDF = %s,
                                    Arrears = %s,
                                    AttendanceBns = %s,
                                    EOY = %s,
                                    Loan = %s,
                                    CarBenefit = %s,
                                    LeaveRef = %s,
                                    SLevy = %s,
                                    SpecialBns = %s,
                                    Lateness = %s,
                                    EducationRel = %s,
                                    SpeProBns = %s,
                                    NPS = %s,
                                    MedicalRel = %s,
                                    Payable = %s,
                                    Deduction = %s,
                                    NetPay = %s,
                                    NetPaysheet = %s,
                                    CurrentGross = %s,
                                    cGrossTax = %s,
                                    PrevGross = %s,
                                    PrevIET = %s,
                                    IET = %s,
                                    NetCh = %s,
                                    CurrentPAYE = %s,
                                    PrevPAYE = %s,
                                    PAYE = %s,
                                    eCSG = %s,
                                    eNSF = %s,
                                    eLevy = %s,
                                    PRGF = %s,
                                    PrevThreshold = %s,
                                    Threshold = %s,
                                    netchar = %s,
                                    CurrentSLevy = %s,
                                    PrevSLevy = %s,
                                    slevyPay = %s,
                                    Absences = %s
                                    WHERE
                                    UNQ = %s
                                    """
                    
                data2 = [eid, flname, 0 , fixAllow, otherDed, ot, discBns, nsf, otherAllow2, tax, medical, trans, overseas, ntax, edf, arrears, attBns, eoyBns2, loan, car, leave, slevypay, speBns, lateness, education, SpeProBns, nps, Medicalrel, payable, deduction, net, NetPaysheet, cgross, gross,  prevGross, piet, iet, netch, cpaye, ppaye, paye, enps ,ensf, levy, eprgf, pths, ths, netchar, slevy ,plevy, slevypay, ab, UNQ]
                cursor.execute(update_salary, data2)
                print("Update Salary Query Executed")

                update_payslip = """UPDATE payslip
                            SET
                            EmpName = %s,
                            Position = %s,
                            NIC = %s,
                            BasicSalary = %s,
                            TravelAlw = %s,
                            Bonus = %s,
                            Gross = %s,
                            PAYE = %s,
                            NPF = %s,
                            NSF = %s,
                            SLevy = %s,
                            Deduction = %s,
                            NetPay = %s,
                            Payable = %s,
                            NetPayAcc = %s,
                            eNPF = %s,
                            eNSF = %s,
                            eLevy = %s,
                            ePRGF = %s,
                            month = %s
                            WHERE
                            UNQ = %s;
                            """
                data_payslip = [flname, pos, nic, 0, trans, bonus, paygross, paye, nps, nsf, slevypay, totalDeduction, netpay, netpay, netpay,  enps, ensf, levy, eprgf, "EOY", UNQ]
                cursor.execute(update_payslip, data_payslip)
                print("Update Payslip Query Executed")
                # msg = "Processing Complete"
                
                emolument = int(basic) + int(arrears) + int(overseas) + int(otherAllow) + int(car) + int(ot) + int(eoy) + int(leave) + int(fixAllow) + int(discBns) + int(SpeProBns) + int(speBns) 

                update_payecsv = """UPDATE payecsv
                                    SET
                                    EmployeeID = %s,
                                    LastName = %s,
                                    FirstName = %s,
                                    Emoluments = %s,
                                    PAYE = %s,
                                    SLevy = %s,
                                    EmolumentsNet = %s
                                    WHERE
                                    UNQ = %s;
                                    """

                data4 = [eid, lname, fname, emolument, paye, slevypay, emolument, UNQ]
                cursor.execute(update_payecsv, data4)
                print("Update PAYE CSV Query Executed")

                msg = "End Of Year Bonus Re-Processing Complete For " + flname + " "
                
            else:
                msg = "No Data Available (Process Bonus First)"
            print("Before Render")
            return render_template("eoy.html",msg=msg, eid = emp_id2, name=flname_all, length = length)
        except Error as e:
                print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    else:
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            query1 = "SELECT EmployeeID FROM employee WHERE Working = 'Yes'"
            cursor.execute(query1)
            emp_id = cursor.fetchall()
            emp_id2 = []
            temp = []
            # print(emp_id)

            for i in range(len(emp_id)):
                temp = ''.join(emp_id[i])
                emp_id2.append(temp)
            
            print(emp_id2)


            query2 = "SELECT FirstName FROM employee WHERE Working = 'Yes'"
            cursor.execute(query2)
            fname = cursor.fetchall()
            fname2 = []
            temp2 = []

            # print(fname)

            for i in range(len(fname)):
                temp2 = ''.join(fname[i])
                fname2.append(temp2)

            print(fname2)

            query3 = "SELECT LastName FROM employee WHERE Working = 'Yes'"
            cursor.execute(query3)
            lname = cursor.fetchall()
            lname2 = []
            temp3 = []

            # print(lname)

            for i in range(len(lname)):
                temp3 = ''.join(lname[i])
                lname2.append(temp3)
            print(lname2)

            flname1 = []
            flname = []

            for i in range(len(emp_id)):
                flname1 = fname2[i] + " " + lname2[i]
                flname.append(flname1)

            print(flname)

            length = len(flname)

            
        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return render_template("eoy.html", eid = emp_id2, name = flname, length = length)
    return render_template("eoy.html")

@app.route("/payslip", methods=["GET" , "POST"])
def payslip():
    # global connection
    if request.method == "POST" and request.form['action'] == 'word':
        month = request.form["mon"]
        year = request.form["year"]
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            query = "SELECT JoinDate, Company, EmpName, Position, NIC, BasicSalary, TravelAlw, Bonus, Gross, PAYE, NPF, NSF, SLevy , Deduction, NetPay, Payable, NetPayAcc, eNPF, eNSF, eLevy, ePRGF FROM payslip WHERE month = %s"
            data1 =[month]
            cursor.execute(query,data1)
            data = cursor.fetchall()
            length = len(data)
            print(data)
            print(length)

            query2 = "SELECT MONTH(hire)"

            query2 = "SELECT EOY FROM EOY WHERE month = %s"
            cursor.execute(query2, data1)
            EOY = cursor.fetchall()

            if month == "EOY":
                print("In If")
                return render_template("payslipeoy.html", data=data, length=length, month = month, EOY=EOY, year=year)    
            else:
                return render_template("payslip2.html", data=data, length=length, month = month, EOY=EOY, year=year)
            # return render_template("payslip2.html")
        except Error as e:
            print("Error While connecting to MySQL : ", e )
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template("payslip.html")

@app.route("/paysheet", methods=["GET" , "POST"])
def paysheet():
    # global connection
    # For Pdf Generate
    if request.method == "POST" and request.form['action'] == 'pdf':
        month = request.form["mon"]
        year = request.form["year"]
        print(month)
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            data1 = [month]
            data2 = [year]
            # query1 = "SELECT * FROM paysheet"
            # query1 = "SELECT EmployeeName, BasicSalary, Arrears, Overseas, TravelAllow, OtherAllow, Gross, PAYE, CSG, NSF, Medical, SLevy, Net FROM paysheet"
            if month == "EOY":
                query1 = "SELECT Employee, BasicSalary, LeaveRef, EOY, Transport, Overseas, OtherAllow, Payable, paye, csg, nsf, slevy, otherDed, Net FROM EOY WHERE month = %s"  
            else:  
                query1 = "SELECT EmployeeName, BasicSalary, LeaveRef, EOY, Transport, Overseas, OtherAllow, Payable, PAYE, NPS, NSFEmpee, SLevy, OtherDeduction, NetPaysheet FROM salary WHERE Month = %s "
            cursor.execute(query1,data1)
            data = cursor.fetchall()
            
            session["data"] = data
            length = len(data)
            
            for i in range(len(data1)):
                month = ' '.join(data1[i])

            for i in range(len(data2)):
                year = ' '.join(data2[i])
            
            # return month
            return render_template("paysheet2.html", data=data, length=length, month = month, year = year)
            # return redirect(url_for('download', data = data))
        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        
    # For Excel Generate

    if request.method == "POST" and request.form['action'] == 'excel':
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            # query1 = "SELECT * FROM paysheet"
            query1 = "SELECT EmployeeName, BasicSalary, Arrears, Overseas, TravelAllow, OtherAllow, FixedAllow, Gross, PAYE, CSG, NSF, Medical, SLevy, Net FROM paysheet"
            cursor.execute(query1)
            data = cursor.fetchall()
            print(data)
            session["data"] = data
            return render_template("paysheet2.html", data=data,month = month)
        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    if request.method == "POST" and request.form['action'] == 'back':
        return render_template("paysheet.html")
    
    return render_template("paysheet.html") 

@app.route('/payecsv', methods=["GET", "POST"])
def payecsv():
    if request.method == "POST" and request.form['action'] == 'paye':
        mon = request.form["mon"]
        year = request.form["year"]
        try:
            connection = mysql.connector.connect(host='careedge-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_DcLCL7NY4AXwTX8d-Jj') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            data1 = [mon]
            # query1 = "SELECT * FROM paysheet"
            # query1 = "SELECT EmployeeName, BasicSalary, Arrears, Overseas, TravelAllow, OtherAllow, Gross, PAYE, CSG, NSF, Medical, SLevy, Net FROM paysheet"
            query1 = "SELECT EmployeeID, LastName, FirstName, Emoluments, PAYE, working, SLevy, EmolumentsNet FROM payecsv WHERE Month = %s "
            cursor.execute(query1,data1)
            data = cursor.fetchall()
            print(data)
            session["data"] = data
            length = len(data)
            print(length)
            return render_template("payecsv2.html", data=data, length=length, month = mon, year= year)
            # return redirect(url_for('download', data = data))
        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    
    return render_template("payecsv.html")


@app.route("/prgfcsv", methods=["GET", "POST"])
def prgfcsv():
    if request.method == "POST" and request.form['action'] == 'prgf':
        mon = request.form["mon"]
        year = request.form["year"]
        data = [mon]
        try:
            connection = mysql.connector.connect(host='demo-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_PcXvrtUuNMOXoepk9DT') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            data2 = [year]
            for i in range(len(data)):
                month = ' '.join(data[i])

            for i in range(len(data2)):
                year = ' '.join(data2[i])

            query = "SELECT EmployeeID, LastName, FirstName, Pension, Working, Hire, Basic, Allowance, Commission, TotalRem, PRGF, reason FROM prgfcsv WHERE month = %s"
            cursor.execute(query,data)
            prgf = cursor.fetchall()

            length = len(prgf)

            return render_template("prgfcsv2.html", length = length, data= prgf, month = month, year = year)        

            
        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template("prgfcsv.html")


@app.route("/cnpcsv", methods=["GET", "POST"])
def cnpcsv():
    if request.method == "POST" and request.form['action'] == 'cnp':
        mon = request.form["mon"]
        year = request.form["year"]
        data = [mon]
        try:
            connection = mysql.connector.connect(host='demo-do-user-12574852-0.b.db.ondigitalocean.com',
                                                    database='defaultdb',
                                                    user='doadmin',
                                                    port='25060',
                                                    password='AVNS_PcXvrtUuNMOXoepk9DT') # @ZodiaX1013
            cursor = connection.cursor(buffered=True)

            data2 = [year]
            for i in range(len(data)):
                month = ' '.join(data[i])

            for i in range(len(data2)):
                year = ' '.join(data2[i])

            query = "SELECT EmployeeID, LastName, FirstName, Basic, Basic2, Season, Alphabet, Number, Working, Blank1, Blank2 FROM cnpcsv WHERE month = %s"

            cursor.execute(query,data)
            cnp_data = cursor.fetchall()

            length = len(cnp_data)

            query2 = "SELECT totalRem FROM cnpcsv WHERE month = %s"
            cursor.execute(query2, data)
            total = cursor.fetchall()

            total = total[0][0]

            query3 = "SELECT CNP FROM cnpcsv WHERE month = %s"
            cursor.execute(query3, data)
            cnp = cursor.fetchall()

            cnp = cnp[0][0]

            return render_template("cnpcsv2.html", length = length, data= cnp_data, month = month, year = year, total=total, cnp=cnp)        

            
        except Error as e:
            print("Error While connecting to MySQL : ", e)
        finally:
            connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return render_template("cnpcsv.html")
    
@app.route('/download')
def download():
    
    if "data" in session:
        print("In IF")
        data = session["data"]
    rendered = render_template('demo.html')
    options = {
        'page-size': 'A3',
        'margin-top': '0.75in',
        'margin-right': '0.5in',
        'margin-bottom': '0.75in',
        'margin-left': '0.1in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'no-outline': None
    }
    config = pdfkit.configuration(wkhtmltopdf='https://github.com/ZodiaX1013/dlgpayroll/blob/main/wkhtmltopdf')
    pdfkit.from_url('https://www.youtube.com/', 'out-test.pdf', configuration=config)
    # config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

    # pdf = pdfkit.from_string(rendered,'paysheet.pdf' , False, configuration=config)
    # response = make_response(pdf)
    # response.headers["Content-Type"] = "application/pdf"
    # response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    
    # return render_template('paysheet2.html',filename='css/style.css', data=data)
    # p = "./paysheet.pdf"
    return "Ready"

    
if __name__ == "__main__":
    app.run(debug=True)