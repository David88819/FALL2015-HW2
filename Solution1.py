__author__ = 'David'
import sys, getopt, csv, datetime, time, math
from scipy.interpolate import interp1d
import numpy as np

def read_args(ls_argv):

    ls_opts, ls_args = getopt.getopt(ls_argv,"d:i:o:y:",)
    for opts, arg in ls_opts:
        if opts == '-d':
            date = arg
        elif opts == '-i':
            input_file = arg
        elif opts == '-o':
            output_file = arg
        elif opts == '-y':
            yield_curve = arg

    date_time = datetime.datetime.strptime(date,'%Y%m%d')
    date = time.mktime(date_time.timetuple())


    bonds = open(input_file,'r')
    yield_c = open(yield_curve,'r')
    data = csv.reader(bonds)
    yield_c1 = csv.reader(yield_c)
    x=[0]
    y=[0]
    for time1 in yield_c1:
        if time1[0] == 'Tenor':
            continue
        x.append(float(time1[0]))
        y.append(float(time1[1])/100.0)
    f = interp1d(x, y)


    bonds_results = open(output_file, 'w')
    out_file = csv.writer(bonds_results)
    for i in data:
        if i[0] == 'id':
            continue
        date_time = datetime.datetime.strptime(i[3],'%Y%m%d')
        i[3] = time.mktime(date_time.timetuple())
        id, price, yield_par, duration, convexity = bond_price(f,i[0],i[1],i[2],i[3] - date,i[4],i[5])
        out_file.writerow((id, price, yield_par, duration, convexity))




def bond_price( f, id , type , notional, maturity , rate , compounding):
    id = int(id)
    notional = float(notional)
    maturity = float(maturity)/(365.0*86400.00)
    rate = float(rate)/100.0
    compounding = 1.0/float(compounding)
    coupon_date = [maturity]
    while (maturity >= compounding):
        maturity = maturity - compounding
        coupon_date.append(maturity)
    coupon_date.sort()
    price = 0.0
    duration = 0.0
    convexity = 0.0
    
    
    if type == 'FLOAT':
        price = notional * (1 + rate * compounding) * math.exp(coupon_date[0] * f(coupon_date[0]))
        yield_par = math.log(1 + rate * compounding)/maturity
        duration = coupon_date[0]
        convexity = coupon_date[0] * coupon_date[0]

    elif type == 'FIXED':
        for i in coupon_date:
            price = price + notional * rate * compounding*math.exp(-i* f(i))
        price = price + notional * math.exp(-coupon_date[len(coupon_date)-1]* f(coupon_date[len(coupon_date)-1]))

        yield_old = 0.00
        yield_new = 0.01
        while (abs(yield_new - yield_old) > 1E-6):
            sum = 0
            sum_prime = 0
            yield_old = yield_new
            for i in coupon_date:
                sum += notional * rate * compounding * math.exp(-i * yield_old)
                sum_prime += -i * notional * rate * compounding * math.exp(-i * yield_old)
            sum += notional * math.exp(-coupon_date[len(coupon_date)-1] * yield_old) - notional
            sum_prime += - coupon_date[len(coupon_date)-1] * notional * math.exp(-coupon_date[len(coupon_date)-1] * yield_old)
            yield_new = yield_old - sum / sum_prime

        yield_par = yield_new

        for i in xrange(len(coupon_date)):
            duration = duration + coupon_date[i] * notional * rate * compounding / float(math.exp(coupon_date[i] * yield_par))
        duration = duration + coupon_date[len(coupon_date)-1] * notional / float(math.exp(coupon_date[len(coupon_date) -1 ] * yield_par))
        duration = duration / float(price)

        for i in xrange(len(coupon_date)):
            convexity = convexity + coupon_date[i]*coupon_date[i] * notional * rate * compounding / float(math.exp(coupon_date[i]*yield_par))
        convexity = convexity + coupon_date[len(coupon_date)-1] * coupon_date[len(coupon_date)-1] * notional / float(math.exp(coupon_date[len(coupon_date) -1 ] * yield_par))
        convexity = convexity / float(price)


    return id, price, yield_par, duration, convexity


if __name__ == "__main__":
      read_args(sys.argv[1:])


