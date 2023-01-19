# In order to use the pydantic package i ran "pip install pydantic" from CMD.  

import re
from pydantic import BaseModel, validator
        
class DnsType(BaseModel):
    name : str 

    @validator("name")
    def is_valid_dns_name(cls, name):
        
        if re.search("[^a-zA-Z0-9.-]", name):
            raise ValueError("Invalid DNS - invalid character was found")
        if len(name) > 253:
            raise ValueError("Invalid DNS - too long name")
    
        labels = name.split(".")

        for i, label in enumerate(labels):
            if len(label) > 63 or len(label) == 0:
                raise ValueError(f"Invalid DNS - label #{i} ({label}) is either empty or too long")            
            if label.isnumeric():
                raise ValueError(f"Invalid DNS - label #{i} ({label}) includes only nunbers")            
            if label[0] == '-' or label[-1] == '-':
                raise ValueError(f"Invalid DNS - the character '-' found at the beginning/end of label #{i} ({label})")            

        return name

class DnsChecker():
    dns : DnsType
    
    def __init__(self, dns_name):
        self.dns = DnsType(name=dns_name)
		
		
def main():
    # Examples of valid DNS hostnames:

    dns_checker_1 = DnsChecker(dns_name="google.com")
    print(dns_checker_1.dns)

    dns_checker_2 = DnsChecker(dns_name="www.google.r3uy.com")
    print(dns_checker_2.dns)


    # Examples of invalid DNS hostnames:
    try:
        DnsChecker(dns_name="google-.com")
    except ValueError as e:
        print(e)
        
    try:
        DnsChecker(dns_name="google.37.com")
    except ValueError as e:
        print(e)
        
if __name__ == "__main__":
    main()		
		



