from ussd import ussd

def run_ussd():
    ussd.run(port=1035)

if __name__ == '__main__':
    run_ussd()