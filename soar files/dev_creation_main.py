import os
import json

def get_current_mod_name(current_dir):
    json_path = os.path.join(current_dir, "dev-data", "datamain.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("mod_name", "My Mod").strip()
        except Exception:
            pass
    return "My Mod"

def update_json_file(current_dir, clean_name):
    json_dir = os.path.join(current_dir, "dev-data")
    json_path = os.path.join(json_dir, "datamain.json")
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}
    except Exception:
        data = {}

    data["mod_name"] = clean_name
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"[2/2] Updated JSON config to: '{clean_name}'")
        return True
    except Exception as e:
        print(f"[!] Error writing to JSON file: {e}")
        return False

def rename_mod(mod_name):
    clean_name = mod_name.strip()
    if not clean_name:
        print("Error: Mod name cannot be empty.")
        return

    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_target_name = get_current_mod_name(current_dir)
        
        items = os.listdir(current_dir)
        old_folder_path = None
        normalized_target = "".join(current_target_name.split()).lower()
        
        for item in items:
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):
                if "".join(item.split()).lower() == normalized_target:
                    old_folder_path = item_path
                    break
                    
        if not old_folder_path:
            old_folder_path = os.path.join(current_dir, current_target_name)

        if not os.path.exists(old_folder_path) and normalized_target != "mymod":
            for item in items:
                if "".join(item.split()).lower() == "mymod":
                    old_folder_path = os.path.join(current_dir, item)
                    break

        if not os.path.exists(old_folder_path):
            print(f"\nError: Could not find your mod folder anywhere.")
            return

        new_folder_path = os.path.join(current_dir, clean_name)
        print(f"[1/2] Renaming folder to: {clean_name}...")
        os.rename(old_folder_path, new_folder_path)
        update_json_file(current_dir, clean_name)
        print("----------------------------------------")
        print("Mod track and rename updated successfully!")
        print("----------------------------------------")
        
    except Exception as e:
        print(f"Error handling mod update: {e}")

def package_mod():
    import shutil
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_mod = get_current_mod_name(current_dir)
        mod_folder_path = os.path.join(current_dir, current_mod)

        if not os.path.exists(mod_folder_path):
            print(f"[!] Error: Active mod folder '{current_mod}' not found to package.")
            return

        zips_dir = os.path.join(current_dir, "Zips")
        if not os.path.exists(zips_dir):
            os.makedirs(zips_dir)

        for root, dirs, files in os.walk(mod_folder_path):
            if "__pycache__" in dirs:
                shutil.rmtree(os.path.join(root, "__pycache__"))

        print(f"[1/2] Packaging mod folder '{current_mod}'...")
        zip_output_base = os.path.join(zips_dir, current_mod)
        
        shutil.make_archive(zip_output_base, 'zip', current_dir, current_mod)
        
        print(f"[2/2] Saved clean distribution package to: Zips/{current_mod}.zip")
        print("----------------------------------------")
        print("Mod packaged and exported successfully!")
        print("----------------------------------------")

    except Exception as e:
        print(f"Error while packaging mod: {e}")

def load_template_command():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_mod = get_current_mod_name(current_dir)
        mod_folder_path = os.path.join(current_dir, current_mod)

        if not os.path.exists(mod_folder_path):
            print(f"[!] Error: Active mod folder '{current_mod}' not found. Name a mod first!")
            return

        init_path = os.path.join(mod_folder_path, "__init__.py")
        
        init_code = '''import os
import platform

def say_works_sir():
    message = "Works, sir."
    print(f"SOAR: {message}")
    
    current_os = platform.system()
    if current_os == "Darwin":
        os.system(f"say -v Daniel '{message}'")
    else:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(message)
            engine.runAndWait()
        except Exception:
            pass

MOD_COMMANDS = {
    "test": say_works_sir
}

def initialize_addon():
    pass
'''
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(init_code)
        print(f" -> Created compliant command template in {current_mod}/__init__.py")
        print("\n----------------------------------------")
        print("Success! Template generated for Public Edition compatibility.")
        print("----------------------------------------")

    except Exception as e:
        print(f"Error creating template command: {e}")

def load_template_window():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_mod = get_current_mod_name(current_dir)
        mod_folder_path = os.path.join(current_dir, current_mod)

        if not os.path.exists(mod_folder_path):
            print(f"[!] Error: Active mod folder '{current_mod}' not found. Name a mod first!")
            return

        init_path = os.path.join(mod_folder_path, "__init__.py")
        
        init_code = '''import tkinter as tk
import threading

def launch_gui():
    root = tk.Tk()
    root.title("SOAR Mod Window")
    root.geometry("300x150")
    
    label = tk.Label(root, text="Mod Interface Running!", font=("Arial", 14))
    label.pack(pady=20)
    
    btn = tk.Button(root, text="Close", command=root.destroy)
    btn.pack(pady=10)
    
    root.mainloop()

MOD_COMMANDS = {}

def initialize_addon():
    gui_thread = threading.Thread(target=launch_gui, daemon=True)
    gui_thread.start()
'''
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(init_code)
        print(f" -> Created cross-platform GUI window template in {current_mod}/__init__.py")
        print("\n----------------------------------------")
        print("Success! Window addon template generated.")
        print("----------------------------------------")

    except Exception as e:
        print(f"Error creating template window: {e}")

def load_template_addon():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_mod = get_current_mod_name(current_dir)
        mod_folder_path = os.path.join(current_dir, current_mod)

        if not os.path.exists(mod_folder_path):
            print(f"[!] Error: Active mod folder '{current_mod}' not found. Name a mod first!")
            return

        init_path = os.path.join(mod_folder_path, "__init__.py")
        
        init_code = '''import os
import platform
import threading
import time

def background_loop():
    message = "My Bot Mod Running..."
    current_os = platform.system()
    
    while True:
        time.sleep(10)
        print(f"SOAR: {message}")
        
        if current_os == "Darwin":
            os.system(f"say -v Daniel '{message}'")
        else:
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(message)
                engine.runAndWait()
            except Exception:
                pass

MOD_COMMANDS = {}

def initialize_addon():
    bg_thread = threading.Thread(target=background_loop, daemon=True)
    bg_thread.start()
'''
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(init_code)
        print(f" -> Created background loop addon template in {current_mod}/__init__.py")
        print("\n----------------------------------------")
        print("Success! Background loop addon template generated.")
        print("----------------------------------------")

    except Exception as e:
        print(f"Error creating template addon: {e}")

def create_config():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        current_mod = get_current_mod_name(current_dir)
        mod_folder_path = os.path.join(current_dir, current_mod)

        if not os.path.exists(mod_folder_path):
            print(f"[!] Error: Active mod folder '{current_mod}' not found. Name a mod first!")
            return

        config_path = os.path.join(mod_folder_path, "config.json")
        default_config = {
            "mywordvariable": "Hello World",
            "mynumbervariable": 1,
            "myfalsetruevariable": True,
        }
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)
        print(f" -> Created default configuration at {current_mod}/config.json")

        init_path = os.path.join(mod_folder_path, "__init__.py")
        init_code = '''import os
import json
import platform

def load_mod_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def say_works_sir():
    config = load_mod_config()
    message = config.get("custom_alert_message", "Works, sir.")
    bot_name = config.get("bot_name", "SOAR")
    
    print(f"{bot_name}: {message}")
    
    if config.get("voice_enabled", True):
        current_os = platform.system()
        if current_os == "Darwin":
            os.system(f"say -v Daniel '{message}'")
        else:
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(message)
                engine.runAndWait()
            except Exception:
                pass

MOD_COMMANDS = {
    "test": say_works_sir
}

def initialize_addon():
    pass
'''
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(init_code)
        print(f" -> Injected JSON config reader routine into {current_mod}/__init__.py")
        print("\n----------------------------------------")
        print("Success! Configuration management system initialized.")
        print("----------------------------------------")

    except Exception as e:
        print(f"Error creating config generator: {e}")

def main():
    print("====================================")
    print("Soar Developer Mod Creation Tool")
    print("Commands:")
    print(" - Name mod <name>       (Renames active folder & config)")
    print(" - template load command (Generates cross-platform TTS command)")
    print(" - template load addon   (Generates 10s background loop bot)")
    print(" - mod package           (Creates a distributable zip file of the active mod)")
    print(" - create config         (Generates managed JSON configurations)")
    print(" - template load window  (Generates cross-platform GUI window)") 
    print(" - exit                  (Close)")
    print("====================================")

    while True:
        try:
            user_input = input("\nEnter command: ").strip()
            
            if user_input.lower() == 'exit':
                print("Exiting developer tool.")
                break
            elif user_input.lower() == "template load command":
                load_template_command()
            elif user_input.lower() == "template load addon":
                load_template_addon()
            elif user_input.lower() == "template load window":
                load_template_window()
            elif user_input.lower() == "mod package":
                package_mod()
            elif user_input.lower() == "create config":
                create_config()
            elif user_input.lower().startswith("name mod "):
                target_name = user_input[9:]
                rename_mod(target_name)
            else:
                print("Invalid command syntax.")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting developer tool.")
            break

if __name__ == "__main__":
    main()