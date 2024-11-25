def firewall_checklist():
    print("\n--- Firewall Checklist ---")
    
    checklist = {
        "Criteria 1. Review the rulesets": "",
        "Criteria 2. Stateful inspection": "",
        "Criteria 3. Logging": "",
        "Criteria 4. Patches and updates": "",
        "Criteria 6. Compliance with security policy": "",
        "Criteria 7. Block spoofed, private, and illegal IPs": "",
        "Criteria 9. Remote access": "",
        "Criteria 10. File transfers": "",
        "Criteria 12. Egress filtering": "",
        "Criteria 13. Firewall redundancy": "",
    }
    
    for question in checklist.keys():
        while True:  # Loop until valid input is provided
            print(f"\nQuestion: {question}")
            answer = input("Score this Criteria (1 - 5): ")
            
            # Check if the input is valid (numeric and within range)
            if answer.isdigit() and 1 <= int(answer) <= 5:
                checklist[question] = int(answer)  # Store the valid answer as an integer
                break  # Exit the loop for this question
            else:
                print("Invalid input. Please enter a score between 1 and 5.")
    
    print("\nYou have completed the checklist.")
    return checklist
