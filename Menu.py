import boto3
from datetime import datetime
import time
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import smtplib
import os
from twilio.rest import Client
from googlesearch import search
import subprocess

print("""
                   -------------------------
                     WELCOME TO THE FUTURE 
                   -------------------------
""")

print("Press 1 to launch EC2 instance")
print("Press 2 to access logs in the cloud")
print("Press 3 for event-driven architecture for audio transcription")
print("Press 4 to connect Python to MongoDB using Lambda")
print("Press 5 to upload an object to S3")
print("Press 6 to integrate Lambda with S3 and SES to send emails")
print("Press 7 to send an email message using Python code")
print("Press 8 to send an SMS message using Python code")
print("Press 9 to scrape top 5 search results from Google using Python code")
print("press 10 to find the current geo coordinates and location using Python code")
print("press 11 to convert text-to-audio using Python code")
print("press 12 to control the volume of your laptop using Python")
print("press 13 to connect to your mobile and send SMS from your mobile messaging app using Python")
print("press 14 to create a function to send bulk emails using Python")
print("press 15 Change the look and feel of GNome terminal")
print("press 16 To create user and set password")
print("press 17 run linux in the browser")
print("press 18 Run Windows softwares e.g notepad in linux")
print("press 19  Sync two different folders in linux . It should ask the user which folders to sync")
print("press 20 On your cmd you print something and it will be converted to ascii art")
print("press 21 Reading the entire RAM")
print("press 22 to launch a gui program inside docker container")
print("press 23 to launch a python3 program inside docker container")
print("press 24 to run a docker software inside docker container")
print("press 25 to run a webserver inside docker container")
print("press 26 to run a webserver inside docker container & connect to host")
print("press 27 Run a Machine Learning Model in a Docker Container")
print("press 28 SSH in the docker running Conatiner")

x = input("Enter your choice: ")

if int(x) == 1:
    # Initialize EC2 resource
    myec2 = boto3.resource(
        "ec2",
        region_name="ap-south-1",
        aws_access_key_id="key_id",  # It's safer to store credentials in environment variables or AWS credentials file
        aws_secret_access_key="secret_access_key"
    )

    def osLaunch():
        # Launch the EC2 instance
        myec2.create_instances(
            InstanceType="t2.micro",
            ImageId="ami-0cc9838aa7ab1dce7",
            MaxCount=1,
            MinCount=1
        )
        print("EC2 instance launched successfully!")

    # Call the function to launch the EC2 instance
    osLaunch()

elif int(x) == 2:
    def access_cloud_logs():
        # Initialize CloudWatch Logs client with region
        logs = boto3.client(
            'logs',
            region_name="ap-south-1",
            aws_access_key_id="key_id",
            aws_secret_access_key="secret_access_key"
        )
        log_group = input("Enter the CloudWatch log group name: ")
        log_stream = input("Enter the CloudWatch log stream name: ")
        response = logs.get_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            startFromHead=True
        )
        for event in response['events']:
            print(event['message'])

    # Call the function to access cloud logs
    access_cloud_logs()

elif int(x) == 3:
    def event_driven_transcription():
        print("Setting up event-driven transcription...")
        
        # Initialize S3 and Transcribe clients with region
        s3 = boto3.client(
            's3',
            region_name="ap-south-1",
            aws_access_key_id="key_id",
            aws_secret_access_key="secret_access_key"
        )
        transcribe = boto3.client(
            'transcribe',
            region_name="ap-south-1",
            aws_access_key_id="key_id",
            aws_secret_access_key="secret_access_key"
        )
        
        bucket_name = input("Enter the S3 bucket name: ")
        file_key = input("Enter the S3 file key (e.g., audio.mp3): ")
        
        # Create a unique job name using the file name and timestamp
        job_name = f"{file_key.split('.')[0]}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Start the transcription job
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{bucket_name}/{file_key}'},
            MediaFormat='mp3',
            LanguageCode='en-IN',
            OutputBucketName=bucket_name
        )
        
        print(f"Transcription job '{job_name}' started.")
        
        # Wait for the job to complete
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                break
            print("Waiting for transcription to complete...")
            time.sleep(5)
        
        if job_status == 'COMPLETED':
            transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            print(f"Transcription completed. Transcript URI: {transcript_uri}")
            
            # Fetch and print the transcription
            transcript_response = s3.get_object(Bucket=bucket_name, Key=f"{job_name}.json")
            transcript_text = transcript_response['Body'].read().decode('utf-8')
            
            import json
            transcript_data = json.loads(transcript_text)
            print("Transcribed Text:")
            print(transcript_data['results']['transcripts'][0]['transcript'])
        else:
            print(f"Transcription job '{job_name}' failed.")

    # Call the function for event-driven transcription
    event_driven_transcription()

elif int(x) == 4:
    def connect_python_to_mongodb():
        print("Connecting to MongoDB...")
        uri = "mongodb+srv://550pradeepkumar:<db_password>@cluster1.ziyxd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        
        db = client.get_database('NewDb')  # Replace with your database name
        collection = db['Data']  # Replace with your collection name
        
        # Example operation
        document = {'hello': 'kaise ho'}
        collection.insert_one(document)
        
        print("Document inserted into MongoDB.")

    # Call the function to connect Python to MongoDB
    connect_python_to_mongodb()

elif int(x) == 5:
    def upload_object_to_s3():
        s3 = boto3.client('s3')
        file_name_with_path = input("Enter the file name with path to upload: ")
        bucket = input("Enter the S3 bucket name: ")
        file_name = input("Enter the file name to display: ")

        try:
            s3.upload_file(file_name_with_path, bucket, file_name)
            print(f"File '{file_name}' uploaded successfully to '{bucket}'.")
        except Exception as e:
            print(f"Error: {e}")

    # Call the function to upload an object to S3
    upload_object_to_s3()

elif int(x) == 6:
    def lambda_s3_ses_integration():
        s3 = boto3.client('s3')
        file_path = input("Enter the full file path of the email list file: ")
        bucket_name = input("Enter the S3 bucket name: ")
        file_name = os.path.basename(file_path)
        
        try:
            s3.upload_file(file_path, bucket_name, file_name)
            print(f"File '{file_name}' uploaded successfully to S3 bucket '{bucket_name}'.")
            print("Lambda function will be triggered to send emails.")
        except Exception as e:
            print(f"Error uploading file to S3: {e}")

    # Call the function to integrate Lambda with S3 and SES
    lambda_s3_ses_integration()

elif int(x) == 7:
    def send_email():
        email = "550pradeepkumar@gmail.com"
        receiver_email = "hirendrakumar550@gmail.com"
        subject = input("Subject: ")
        message = input("Message: ")

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, "wbrd hglm xclp ecxh")
        server.sendmail(email, receiver_email, f"Subject: {subject}\n\n{message}")

        print("Email has been sent to", receiver_email)

    # Call the function to send an email
    send_email()

elif int(x) == 8:
    # Your Twilio credentials
    account_sid = 'sid'
    auth_token = 'token'
    twilio_number = '+14045864795'
    recipient_number = '+919058430981'

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Send the SMS
    message = client.messages.create(
        body='hii brother',
        from_=twilio_number,
        to=recipient_number
    )

    print(f"Message sent with SID: {message.sid}")

elif int(x) == 9:
    query = input("Enter your search query: ")

    num_results = 5

    search_results = search(query, num_results=num_results)

    for i, result in enumerate(search_results, start=1):
        print(f"{i}. {result}")
        
elif int(x) == 10:
     from geopy.geocoders import Nominatim
     import requests

     # Initialize the geolocator with a user agent
     geolocator = Nominatim(user_agent="geoapiExercises")

     def get_location():
         location = geolocator.geocode("Jaipur, Rajasthan, India")
         if location:
             print(f"Address: {location.address}")
             print(f"Latitude: {location.latitude}")
             print(f"Longitude: {location.longitude}")
         else:
             print("Location not found")

     def get_ip_location():
         response = requests.get("http://ipinfo.io")
         if response.status_code == 200:
             data = response.json()
             print(f"IP Location: {data}")
         else:
             print("Failed to retrieve IP-based location")

     print("Fetching current geo coordinates...")
     get_location()

     print("Fetching IP-based location...")
     get_ip_location()
     
elif int(x) == 11:
     import pyttsx3

     engine = pyttsx3.init()

     text_to_speak = input("Enter text to speak: ")

     engine.setProperty('rate', 160)
     engine.setProperty('volume', 1.0)  # Ensure volume is between 0.0 and 1.0

     engine.say(text_to_speak)
     engine.runAndWait()
     
elif int(x) == 12:
    import subprocess

    def set_volume(percent):
        if percent < 0 or percent > 100:
            print("Volume percentage must be between 0 and 100.")
            return

        # Calculate the volume level as a percentage (0 to 100)
        volume_level = int(percent)

        # Set the volume using amixer
        subprocess.run(["amixer", "sset", "Master", f"{volume_level}%"])
        print(f"Volume set to {percent}%")

    try:
        user_input = float(input("Enter the desired volume percentage (0-100): "))
        set_volume(user_input)
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 100.")

    
elif int(x) == 13:
     import pywhatkit as kit
     kit.sendwhatmsg_instantly("+917452096884", "hii brother", 1, 3)
     

elif int(x) == 14:

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    def send_email(to_email, subject, body, smtp_server, smtp_port, login, password):
        msg = MIMEMultipart()
        msg['From'] = login
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(login, password)
            text = msg.as_string()
            server.sendmail(login, to_email, text)
            server.quit()
            print(f"Email sent to {to_email}")

        except Exception as e:
            print(f"Failed to send email to {to_email}. Error: {str(e)}")

    def send_bulk_emails(recipient_list, subject, body, smtp_server, smtp_port, login, password):
        for recipient in recipient_list:
            send_email(recipient, subject, body, smtp_server, smtp_port, login, password)

    # Define email details
    subject = "Hi, good morning everyone!!!"
    body = "This is a test email sent in bulk."
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    login = "550pradeepkumar@gmail.com"
    password = "wbrd hglm xclp ecxh"  # Be cautious with hardcoding passwords

    # List of recipient emails
    recipient_list = [
        "gungunkhandelwal12@gmail.com",
        "bhupesh7750@gmail.com",
        "samirsinghjadon17@gmail.com",
        "anurag1342001@gmail.com"
    ]

    # Send the emails
    send_bulk_emails(recipient_list, subject, body, smtp_server, smtp_port, login, password)
    

if int(x) == 15:

    import subprocess

    def set_terminal_profile_colors(profile_name):
        # Get the profile ID based on the profile name
        try:
            profile_list_cmd = "gsettings get org.gnome.Terminal.ProfilesList list"
            profile_list_output = subprocess.check_output(profile_list_cmd, shell=True).decode('utf-8')
            profile_ids = eval(profile_list_output)

            profile_id = None
            for pid in profile_ids:
                name_cmd = f"gsettings get org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{pid}/ visible-name"
                name_output = subprocess.check_output(name_cmd, shell=True).decode('utf-8').strip().strip("'")
                if name_output == profile_name:
                    profile_id = pid
                    break

            if profile_id is None:
                print(f"Profile '{profile_name}' not found.")
                return

            # Set the colors
            background_color = "rgba(0,0,0,0.9)"
            foreground_color = "rgba(255,255,255,1)"
            palette = [
                "#2e3436", "#cc0000", "#4e9a06", "#c4a000", "#3465a4", "#75507b", "#06989a", "#d3d7cf",
                "#555753", "#ef2929", "#8ae234", "#fce94f", "#729fcf", "#ad7fa8", "#00f5d4", "#eeeeec"
            ]

            subprocess.run([
                "gsettings", "set", f"org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{profile_id}/", 
                "background-color", background_color
            ], check=True)
            subprocess.run([
                "gsettings", "set", f"org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{profile_id}/", 
                "foreground-color", foreground_color
            ], check=True)
            subprocess.run([
                "gsettings", "set", f"org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{profile_id}/", 
                "palette", str(palette).replace('"', "'")
            ], check=True)

            print(f"Colors set successfully for profile '{profile_name}'.")

        except subprocess.CalledProcessError as e:
            print(f"Error setting colors: {e}")

    # Replace 'pradeep kumar' with your actual profile name
    set_terminal_profile_colors("pradeep kumar")
    

elif int(x) == 16:
    import subprocess
    import getpass

    def create_user(username, password):
        try:
            # Create the user
            subprocess.run(['sudo', 'useradd', username], check=True)

            # Set the password
            subprocess.run(['sudo', 'chpasswd'], input=f'{username}:{password}', text=True, check=True)

            print(f"User '{username}' created and password set successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

    def main():
        username = input("Enter the username to create: ")
        password = getpass.getpass("Enter the password for the user: ")
        create_user(username, password)

    if _name_ == "_main_":
        main()

elif int(x) == 17:

    import subprocess

    def run_terminal_in_browser():
        try:
            # Check if ttyd is installed
            result = subprocess.run(['which', 'ttyd'], capture_output=True, text=True)
            if not result.stdout.strip():
                print("ttyd is not installed. Please install it first.")
                return

            # Define the command to run ttyd with bash
            command = ['ttyd', '-p', '8080', '/bin/bash']

            # Run the command to start the terminal in the browser
            print("Starting ttyd... Access your terminal at http://localhost:8080")
            subprocess.run(command)

        except Exception as e:
            print(f"An error occurred: {e}")

    if _name_ == "_main_":
        run_terminal_in_browser()
        
elif int(x) == 18:
    import subprocess

    # Command to run Notepad using Wine
    command = ['wine64', 'notepad']

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print("Notepad launched successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        
elif int(x) == 19:

    import os
    import shutil

    def check_dir(path):
        """Check if the given path is a directory."""
        if not os.path.isdir(path):
            print(f"Directory {path} does not exist.")
            exit(1)

    def sync_directories(src_dir, dest_dir):
        """Sync contents from src_dir to dest_dir."""
        for root, dirs, files in os.walk(src_dir):
            # Calculate the destination directory
            dest_root = os.path.join(dest_dir, os.path.relpath(root, src_dir))
            if not os.path.exists(dest_root):
                os.makedirs(dest_root)

            # Copy files
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_root, file)
                shutil.copy2(src_file, dest_file)
                print(f"Copied {src_file} to {dest_file}")

        # Remove files from the destination that are not in the source
        for root, dirs, files in os.walk(dest_dir):
            rel_path = os.path.relpath(root, dest_dir)
            src_root = os.path.join(src_dir, rel_path)
            if not os.path.exists(src_root):
                for file in files:
                    os.remove(os.path.join(root, file))
                    print(f"Removed {os.path.join(root, file)}")

    def main():
        # Prompt user for source directory
        src_dir = input("Enter the path of the source directory: ").strip()
        check_dir(src_dir)

        # Prompt user for destination directory
        dest_dir = input("Enter the path of the destination directory: ").strip()
        check_dir(dest_dir)

        # Sync the directories
        print(f"Syncing {src_dir} to {dest_dir}...")
        sync_directories(src_dir, dest_dir)
        print("Sync complete.")

    if _name_ == "_main_":
        main()
    
elif int(x) == 20:

    from pyfiglet import Figlet

    def text_to_ascii_art(text):
        figlet = Figlet()
        ascii_art = figlet.renderText(text)
        return ascii_art

    if _name_ == "_main_":
        # Prompt the user for input text
        text = input("Enter the text you want to convert to ASCII art: ")

        # Convert the text to ASCII art
        ascii_art = text_to_ascii_art(text)

        # Print the ASCII art
        print(ascii_art)
        
if int(x) == 21:
   import psutil

   def read_ram():
       ram_info = psutil.virtual_memory()
       print(f"Total RAM: {ram_info.total / (1024 ** 3):.2f} GB")
       print(f"Available RAM: {ram_info.available / (1024 ** 3):.2f} GB")
       print(f"Used RAM: {ram_info.used / (1024 ** 3):.2f} GB")
       print(f"RAM Percentage Used: {ram_info.percent}%")

   # Example usage
   if _name_ == "_main_":
       read_ram()




elif int(x) == 22:
    import subprocess

    def gui():
        # List Docker images
        images = subprocess.getoutput("docker images")
        print("Available Docker Images:\n", images)

        # Launch the Docker container with GUI support
        try:
            # Run the container with DISPLAY set to host's display
            launchOS = subprocess.getoutput(
                "docker run -d --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix firefox-gui-programm:v1")

            
            print("Launched container ID:\n", launchOS)
        except Exception as e:
            print("Failed to launch GUI in Docker container:", str(e))

    # Call the function to launch the GUI
    gui()
    
elif int(x) == 23:
    import subprocess
    import os

    def docker():
        try:
            # Step 1: Run the Docker container
            output = subprocess.run(
                ['docker', 'run', '-dit', '--name', 'dind', '-v', '/var/run/docker.sock:/var/run/docker.sock', 'hirendra113/docker:dind'],
                capture_output=True, text=True, check=True
            )
            print("Container started:", output.stdout)

            # Step 2: Execute a command in the running Docker container
            output2 = os.system('docker exec -ti dind /bin/bash')
            print(output2)

        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e}")
            print("Error output:", e.stderr)

    docker()



    
elif int(x) == 24:
    # launch docker inside docker container
    def Dind():
          images=subprocess.getoutput("docker images")
          print(images)
          
          launchOS=subprocess.getoutput("docker run -dit --name dind -v /var/run/docker.sock:/var/run/docker.sock  docker:dind")
          command=os.system("docker exec -it dind /bin/bash")
          result = os.popen(command).read()
          print(result)
    
    Dind()
    
elif int(x) == 25:
    # launch webserver inside docker container
    def webserver():
          
          
          launchOS=subprocess.getoutput("docker run -d --name webserver -ti webserver:v1")
          webos=subprocess.getoutput("docker ps")
          print(launchOS)
          print(webos)
          
    webserver()
    
elif int(x) == 26:

    # launch webserver inside docker container & connect to host
    def webserver2():
        server_running = subprocess.getoutput("docker ps")

        if "webserverHost" in server_running:
            print("webserver is running")
        else:
            launchOS = subprocess.getoutput("docker run -d --name webserverHost -ti -p 1234:80 webserver:v1")
            webos = subprocess.getoutput("docker ps")
            print(launchOS)
            print(webos)

    webserver2()
    
elif int(x) == 27:

    def webserver2():
        try:
            launchOS = subprocess.getoutput("docker run -it ml-python:v1")
            print(launchOS)

            webos = subprocess.getoutput("docker ps")
            print(webos)
        except subprocess.CalledProcessError as e:
            print(f"Error running Docker command: {e}")

    webserver2()
    
elif int(x) == 28:

    import os
    import subprocess
    import paramiko
    import time

    # Updated Dockerfile content
    dockerfile = """
    FROM ubuntu:latest

    # Install OpenSSH server
    RUN apt-get update && apt-get install -y openssh-server

    # Create the required privilege separation directory
    RUN mkdir -p /run/sshd

    # Set the root password
    RUN echo 'root:password' | chpasswd

    # Allow root login and password authentication
    RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
    RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

    # Expose SSH port
    EXPOSE 22

    # Start the SSH service when the container starts
    CMD ["/usr/sbin/sshd", "-D"]
    """

    # Step 1: Write the Dockerfile to a temporary file
    with open("Dockerfile", "w") as f:
        f.write(dockerfile)

    # Step 2: Build Docker image
    print("Building Docker image...")
    build_command = "docker build -t ubuntu-ssh ."
    subprocess.run(build_command, shell=True, check=True)

    # Step 3: Run Docker container and map port 22 to a host port
    print("Running Docker container...")
    run_command = "docker run -d -p 2222:22 --name my_ssh_container ubuntu-ssh"
    subprocess.run(run_command, shell=True, check=True)

    # Step 4: Wait for the container to start
    time.sleep(5)

    # Step 5: Fetch the Docker container logs to verify SSH server status
    print("Fetching Docker container logs...")
    logs_command = "docker logs my_ssh_container"
    container_logs = subprocess.getoutput(logs_command)
    print("Container logs:\n", container_logs)

    # User input for SSH connection details
    hostname = "localhost"
    port = 2222  # Host port mapped to the container's port 22
    username = input("Enter SSH username: ")
    password = input("Enter SSH password: ")

    print(f"Trying to SSH into the container at {hostname}:{port} with username '{username}'...")

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Attempt to connect
        ssh.connect(hostname, port=port, username=username, password=password)

        # Run a command inside the container via SSH
        stdin, stdout, stderr = ssh.exec_command('ls /')
        print("Command Output:")
        print(stdout.read().decode())

        ssh.close()

    except paramiko.AuthenticationException:
        print("Error: Authentication failed. Please check the credentials or SSH configuration.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    
    


else:
    print("Invalid choice. Please enter a valid option.")