import pyaudio

def list_all_microphones():
    """Lists all available microphones and their indices."""
    try:
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        microphones = {}
        for i in range(0, numdevices):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            if (device_info.get('maxInputChannels')) > 0:
                microphones[i] = device_info.get('name')

        p.terminate()

        if microphones:
            return microphones
        else:
            print("No microphones found.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        if 'p' in locals():
          p.terminate()
        return None

def get_default_microphone_index():
    """Gets the index of the default microphone."""
    mics = list_all_microphones()
    if mics:
        for index, name in mics.items():
            if 'default' in name.lower(): # Check for "default" in the name (case-insensitive)
                return index
        # If no microphone with "default" in the name is found, return the first one
        return list(mics.keys())[0]
    return None


def select_microphone():
    """Allows the user to select a microphone or use the current default."""

    default_mic_index = get_default_microphone_index()
    all_mics = list_all_microphones()

    if not all_mics:
        print("No microphones found. Exiting.")
        return None

    print("Current Selected Microphone:")
    if default_mic_index is not None and default_mic_index in all_mics:
        print(f"Index: {default_mic_index}, Name: {all_mics[default_mic_index]}")
    else:
        print("No selected microphone found.")


    print("\nAvailable Microphones:")
    for index, name in all_mics.items():
        print(f"Index: {index}, Name: {name}")

    while True:
        choice = input("\nEnter the index of the microphone you want to use, or press Enter to use the current default: ")
        if choice == "":
            if default_mic_index is not None:
                return default_mic_index
            else:
                print("No selected microphone available. Please select a microphone.")
                continue  # Ask for input again

        try:
            selected_index = int(choice)
            if selected_index in all_mics:
                print("You will be using microphone:")
                if selected_index is not None and selected_index in all_mics:
                    print(f"Index: {selected_index}, Name: {all_mics[selected_index]}")
                else:
                    print("No microphone selected.")
                return selected_index
            else:
                print("Invalid microphone index. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or press Enter.")

if __name__ == "__main__":
    selected_mic = select_microphone()    

