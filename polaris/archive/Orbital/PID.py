print(r"""\ 
          ______  _______  ______        __    _____          __           __
         / ___/ |/ / ___/ /_  __/__ ___ / /_  / ___/__  ___  / /________  / /
        / (_ /    / /__    / / / -_|_-</ __/ / /__/ _ \/ _ \/ __/ __/ _ \/ / 
        \___/_/|_/\___/   /_/  \__/___/\__/__\___/\___/_//_/\__/_/  \___/_/  
        | | / /__ _______ (_)__  ___    <  // _ \                           
        | |/ / -_) __(_-</ / _ \/ _ \   / // // /                           
        |___/\__/_/ /___/_/\___/_//_/  /_(_)___/                            
                                                                    """)
test_selected = input("Please select a test to run:\n 1. Equality test\n 2. Left thrust test\n 3. Right thrust test\n 4. Open nozzle until empty test\n")

if test_selected == "1":
    print("Running Equality test")
    #test1()
    print("Test complete")
elif test_selected == "2":
    print("Running Left thrust test")
    #test2()
    print("Test complete")
elif test_selected == "3":
    print("Running Right thrust test")
    #test3()
    print("Test complete")
elif test_selected == "4":
    print("Running Open nozzle until empty test")
    #test4()
    print("Test complete")
