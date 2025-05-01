from HQ.commands import handle_command

def run_cli():
    print("Welcome to Ragent CLI (Blane Interface)")
    while True:
        try:
            user_input = input("(Blane) > ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("(Blane) > Goodbye!")
                break
            handle_command(user_input)
        except KeyboardInterrupt:
            print("\n(Blane) > Interrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"(Blane) > Error: {e}")

if __name__ == "__main__":
    run_cli()
