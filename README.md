AWS EC2	https://aws.amazon.com/console/	
		
		
	EC2	
	launch instance	
	select ubuntu	
	Amazon machine image keep as is	
	instance type use t2.large  8GB memory 	
	create new key pair 	
	key pair name	mcqkey
	type: RSA, type .pem	
	downloaded and saved at	"G:\My Drive\backup jerry-200k(master copy)\AI\mcqkey.pem"
	clike allow HTTPS traffic from the internet 	
	allow HTTP traffic from the internet 	
	config storage to 16GB	
	then launch instance	
	public ipv4	3.145.35.116
	click on the instance id	
	then click connect	
	then click connect again(on next page). 	
	(machine is launched)	
in the machine:		
run	sudo apt update	to run a command as user root:  sudo <command>
to see the list:	apt list --upgradable	(optional check)
	sudo apt-get update	
	sudo apt upgrade -y	
	sudo apt install git curl unzip tar make sudo vim wget  python3-pip -y	
	git clone <git project link>	
	pip install -r requirements.txt --break-system-package 	
	need to manually create .env file. 	
		
	need to open up the port 8501 first 	
	go to portal, that instance -> security -> security group -> edit inbound rules 	
	add rules:  source type custom tcp; 8501 ; 0.0.0.0/0	
		
	python3 -m streamlit run StreamlitApp.py 	
		
	
		

