import re
import sys
import getpass 

def calculate_strength(password):
    """Calculate password strength score and provide feedback"""
    
    score = 0
    feedback = []
    suggestions = []

    length = len(password)
    if length >= 12:
        score += 3
        feedback.append("✓ Great length (12+ characters)")
    elif length >= 8:
        score += 2
        feedback.append("✓ Good length (8-11 characters)")
        if length < 12:
            suggestions.append("Consider making it 12+ characters for better security")
    else:
        feedback.append("✗ Too short (minimum 8 characters required)")
        suggestions.append("Make your password at least 8 characters long")
    
    if re.search(r"[A-Z]", password):
        score += 1
        feedback.append("Contains uppercase letters")
    else:
        feedback.append(" Missing uppercase letters")
        suggestions.append("Add at least one UPPERCASE letter (A-Z)")
    
    if re.search(r"[a-z]", password):
        score += 1
        feedback.append("Contains lowercase letters")
    else:
        feedback.append(" Missing lowercase letters")
        suggestions.append("Add at least one lowercase letter (a-z)")

    if re.search(r"\d", password):
        score += 1
        feedback.append("Contains numbers")
    else:
        feedback.append("Missing numbers")
        suggestions.append("Add at least one number (0-9)")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 2  # Extra point for special chars
        feedback.append("Contains special characters")
    else:
        feedback.append("Missing special characters")
        suggestions.append("Add at least one special character (!@#$%^&*)")
    
    common_patterns = [
        "123", "abc", "qwerty", "password", "admin", "welcome",
        "111", "000", "123456", "654321", "2023", "2024"
    ]
    
    pattern_found = False
    for pattern in common_patterns:
        if pattern.lower() in password.lower():
            score -= 2  # Penalty for common patterns
            feedback.append("⚠ Contains common pattern")
            suggestions.append(f"Avoid common sequences like '{pattern}'")
            pattern_found = True
            break
    
    if re.search(r'(.)\1{2,}', password):  # 3+ repeated chars
        score -= 1
        feedback.append("⚠ Too many repeated characters")
        suggestions.append("Avoid repeating the same character many times")
    
    with open('common_passwords.txt', 'r') as f:
        common_passwords = [line.strip().lower() for line in f]
    
    if password.lower() in common_passwords:
        score = 0  # Reset to zero for very common passwords
        feedback.append("VERY WEAK: This is a commonly used password")
        suggestions.append("Choose a completely unique password")
    
    max_score = 9  # 3+1+1+1+2+1 (length+upp+low+dig+special+bonus)
    percentage = (score / max_score) * 100 if max_score > 0 else 0
    
    if percentage >= 85:
        rating = "STRONG "
        color = "\033[92m"  
    elif percentage >= 60:
        rating = "MODERATE "
        color = "\033[93m"
    else:
        rating = "WEAK "
        color = "\033[91m" 
    
    return {
        "score": score,
        "max_score": max_score,
        "percentage": percentage,
        "rating": rating,
        "color": color,
        "feedback": feedback,
        "suggestions": suggestions,
        "length": length
    }

def estimate_crack_time(password):
    """Very basic crack time estimation (educational)"""
    length = len(password)
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[^A-Za-z0-9]', password))
    
    charset_size = 0
    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_special: charset_size += 32 
    
    if charset_size == 0:
        return "instant"
    
    combinations = charset_size ** length
    guesses_per_second = 1_000_000_000  # 1 billion guesses/sec (modern cracking)
    seconds = combinations / guesses_per_second
    
    if seconds < 1:
        return "less than a second"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours"
    elif seconds < 31536000:  # 1 year
        return f"{int(seconds/86400)} days"
    else:
        return f"{int(seconds/31536000)} years"

def main():
    """Main function"""
    print("\n" + "="*60)
    print("        PASSWORD STRENGTH CHECKER")
    print("="*60)
    print("Educational tool - Your password is NOT sent anywhere\n")
    
    while True:
        print("\n" + "-"*60)
        print("Enter a password to check strength (or 'quit' to exit):")
        
        # Use getpass for hidden input (more secure)
        try:
            password = getpass.getpass("Password: ")
        except:
            # Fallback for environments without getpass
            password = input("Password: ")
        
        if password.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye! Use strong passwords!")
            break
        
        if not password:
            print("\n⚠ Please enter a password")
            continue
        
        print("\n" + "-"*60)
        print("ANALYZING PASSWORD...")
        print("-"*60)
        
        # Calculate strength
        result = calculate_strength(password)
        
        # Show password info (masked)
        masked = password[0] + "*" * (len(password)-2) + password[-1] if len(password) > 2 else "***"
        print(f"\nPassword: {masked}")
        print(f"Length: {result['length']} characters")
        
        # Show crack time estimate
        crack_time = estimate_crack_time(password)
        print(f"Estimated crack time: {crack_time}")
        
        # Show score
        print(f"\nSCORE: {result['score']}/{result['max_score']} ({result['percentage']:.1f}%)")
        print(f"{result['color']}STRENGTH: {result['rating']}\033[0m")
        
        # Show feedback
        print("\nCHECKLIST:")
        for item in result['feedback']:
            print(f"  {item}")
        
        # Show suggestions if any
        if result['suggestions']:
            print("\n💡 SUGGESTIONS TO IMPROVE:")
            for suggestion in result['suggestions'][:3]:  # Top 3 suggestions
                print(f"  • {suggestion}")
        
        # Tips
        print("\n PASSWORD TIPS:")
        print("  • Use a mix of character types")
        print("  • Longer passwords are better (12+ characters)")
        print("  • Avoid personal information")
        print("  • Consider using a passphrase")
        print("  • Use a password manager")
        
        print("\n" + "="*60)
        
        # Ask to continue
        cont = input("\nCheck another password? (y/n): ").lower()
        if cont not in ['y', 'yes']:
            print("\nRemember: Use unique passwords for each account!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Program terminated")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
