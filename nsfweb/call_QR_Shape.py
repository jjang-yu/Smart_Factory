import paramiko

def execute_remote_sh(ssh_host, ssh_port, ssh_user, ssh_password, remote_script_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)
    
    # 원격지에서 .sh 파일 실행
    stdin, stdout, stderr = client.exec_command(f'bash {remote_script_path}')
    print(stdout.read().decode())  # 표준 출력의 내용을 출력
    print(stderr.read().decode())  # 표준 에러의 내용을 출력, 에러가 있다면 확인 가능

    return stdout.read().decode('utf-8')

# SSH 접속 정보
ssh_host = '192.168.1.199'  # 원격 라즈베리 파이의 IP 주소
ssh_port = 22
ssh_user = 'nsf'
ssh_password = '1234'

# 원격 스크립트 경로
#remote_script_path = '/home/nsf/cv_test/QR_Shape.sh'
#execute_remote_sh(ssh_host, ssh_port, ssh_user, ssh_password, remote_script_path)
