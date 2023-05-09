def get_linux_ec2_private_ip():
    response = None
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    from urllib.request import urlopen
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        return response.read().decode("utf-8")
    except:
        return None
    finally:
        if response:
            response.close()



private_ip = get_linux_ec2_private_ip()