https://www.fordham.edu/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/web-application-security-deployment-procedure

# Web Application Security Deployment Procedure

## Version 1.2

**For Students, Faculty, Staff, Guests**

## Purpose

The purpose of this procedure is to deploy web application security controls on the University’s IT Resources.

## Scope

This IT procedure, and all policies referenced herein, shall apply to all members of the Office of Information Technology staff (the “User(s)” or “you”) who use, access, or otherwise employ, locally or remotely, the University’s IT Resources, whether individually controlled, shared, stand-alone, or networked.

## Procedure Statement

System/application owners are responsible for deploying appropriate Web Application Security controls 1 to protect web applications per the

[Web Application IT Security Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/web-application-security-policy/). This document provides the steps necessary to administer web application security controls and policies for all incoming traffic to the University’s web applications to filter out malicious visitors and requests (e.g., SQL injections, XSS attacks, cookie poisoning, denial-of-service attacks, brute force, credential stuffing).


[2](#_ftn2)### A. Authentication

- Verify that hard-coded credentials are not stored within the application code.
- Enable password reset where Central Authentication Service (CAS) cannot be implemented:
- Reset system passwords with challenging questions and answers.
- Password reset options must not reveal the validity of the account.
- Passwords must meet the University’s password requirements as stated in the
[Acceptable Uses of IT Infrastructure and Resources-Policy Statement](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/acceptable-uses-of-it-infrastructure-and-resources-policy-statement/).

- Lock failed account logins after five failed attempts, and accounts must be locked for a minimum of five minutes.
- Authentication error messages must be generic and not disclose any sensitive information regarding the account, such as the validity of the username or password.
- Database credentials (i.e., the authentication credentials in the business logic tier) must be stored in a secure, centralized location on the server outside of the web root. The file should only be readable by the user account running the application.
- Configure applications and middleware services to run with minimal privileges.
- The application must automatically log out the inactive User after 15 minutes unless an extended session is approved by design and accepted by an Office of Information Technology AVP.
- You must destroy corresponding data and session information on the server when the User logs out of the application.
- The logout button or link must be easily accessible to the User on every page after they have authenticated.

### B. Controlled Administrative Privileges

- Use access control checks to mediate all requests to a standard security gateway (i.e., Mandatory Access Control), ensuring that access control checks are triggered whether or not the User is authenticated.
- All decisions must be based on the principle of least privilege.
- Grant access to newly created accounts on a need-to-know basis.
- Do not allow direct object references to files or parameters that can be manipulated to grant access to the system.
- Prevent non-validated forwards/redirects from unauthorized access and phishing by conducting access control checks before sending the User to the location.

### C. Configuration and Operations

- Office of Information Technology’s change management process must be followed so that new software releases are tested and associated documentation is completed before going live.
- Configure the hardening of all infrastructure/application components to satisfy the agreed-upon levels of the vulnerability scanning tools.
- Draft and regularly test a thorough disaster recovery plan to minimize the impact of an incident.

### D. Data Protection

- Disable HTTP access for all SSL-enabled resources.
- Disable weak SSL ciphers.
- Use valid SSL certificates from a reputable certificate authority.
- Use the Strict-Transport-Security header to ensure that the browser does not talk to the server on non-SSL per the
[Server Certificate Security](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/server-certificate-security-policy/)policy. - If database User passwords must be stored (e.g., files), appropriate Access Control Lists (ACLs) must be used.
- Perform critical establishment or exchanges over a secure channel (e.g., password manager, shared drive).
- Securely store keys and make them accessible to the appropriate individuals on a need-to-know basis.
- When appropriate, disable browser data caching using the cache control HTTP headers or Meta tags within the HTML page.
- Turn off the autocomplete setting for sensitive inputs (e.g., login form in the HTML form).

### E. Error Handling and Logging

- Error messages must be generic and not reveal details about the application.
- Suppress default framework error messages or replace them with customized messages.
- Configure error handlers to handle unexpected errors without allowing unhandled exceptions to occur.
- Logging and storage
- All authentication activities, whether successful or not, must be logged, as well as privilege changes and administrative activities.
- All-access to sensitive data such as PII or PHI must be logged and stored centrally in the University’s log management solution (e.g., SumoLogic).
- Log retention must follow the retention policy set forth by the University to meet regulatory requirements per the
[Records Retention and Disposal Policy](/resources/policies/records-retention-and-disposal-policy/)and the[Logging Requirements Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/logging-requirements-policy/#d.en.90949).


### F. Input and Output Handling

- Contextual output encoding
- All input functions must contextually encode data on the server side before the application accepts it.
- Set the encoding using HTTP headers or Meta tags for every page in the application to ensure the page’s encoding is defined, and the browser does not have to determine the encoding on its own.

- Allow lists/block lists
- Allow listing input is the preferred approach; only accept data that meets the criteria.
- Apply to block lists for known harmful input patterns and characteristics for more flexibility.

- SQL Injection
- Must be addressed during application development or as a last resort using a web application firewall to mitigate.
- Create SQL queries with User content passed into a bind variable to prevent attacks.
- Do not dynamically create SQL queries using string concatenation if the SQL query string is used in a bound or parameterized query.

- Tokens for forged requests
- Whenever possible, embed a random value unknown to third parties into the HTML form to prevent cross-site request forgery attacks.
- Require a unique, sever-issued, and randomized token for each request.


### G. File/Input Validation

- Validate the size of the file, the file type, and the file contents (i.e., allow list, allowed file types, antivirus software, renaming files after uploading) when accepting file uploads from the User, and ensure that it is not possible to overwrite the destination path for the file.
- Validate that the source of the input is the authenticated User.

### H. Secure Cookie Attributes

- The session cookie must be set with both the HTTP only and the secure flags.
- Set the cookie domain and path scope to the most restrictive settings for the application.
- Do not use wildcard domain-scoped cookies.
- Session cookies must have a reasonable session expiration time.
- Avoid non-expiring session cookies.

1 Open Web Application Security Project

[(OWASP) Top 10 Proactive Controls](https://owasp.org/www-project-proactive-controls/)and

[OWASP Mobile Security Project](https://owasp.org/www-project-mobile-app-security/).

[2](#_ftnref2)[OWASP](https://owasp.org/) offers best practices for addressing critical web application security risks.

## Definitions

**Cookie Poisoning** is the modification of a cookie (personal information on a web User's computer) by an attacker to gain unauthorized information about the User for purposes such as identity theft. The attacker may use the information to open new accounts or to gain access to the User's existing accounts.

**Credential Stuffing** is the automated injection of breached username/password pairs to gain access to User accounts fraudulently. This is a subset of the brute force attack category: large numbers of spilled credentials are automatically entered into websites until they are potentially matched to an existing account, which the attacker can then hijack for their purposes.

**Cross-Site Scripting (XSS)** attacks are a type of injection in which malicious scripts are injected into otherwise benign and trusted websites. XSS attacks occur when an attacker uses a web application to send malicious code, generally in the form of a browser-side script, to a different end-user. Flaws that allow these attacks to succeed are quite widespread and occur anywhere a web application uses input from a User within the output it generates without validating or encoding it.

**Denial-of-service attack (DoS attack)** is a cyber-attack where the perpetrator seeks to make a machine or network resource unavailable to its intended Users by temporarily or indefinitely disrupting the services of a host connected to the internet.

**IT Resources** include computing, networking, communications, application, and telecommunications systems, infrastructure, hardware, software, data, databases, personnel, procedures, physical facilities, cloud-based vendors, Software as a Service (SaaS) vendors, and any related materials and services.

**SQL Injection** is a code injection technique used to attack data-driven applications, in which malicious SQL statements are inserted into an entry field for execution (e.g., to dump the database contents to the attacker).

**Web Application Security** is a branch of information security that deals specifically with the security of websites, web applications, and web services.

## Related Policies and Procedures

[Acceptable Uses of IT Infrastructure and Resources-Policy Statement](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/acceptable-uses-of-it-infrastructure-and-resources-policy-statement/)[Change Control Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/change-control-policy/)[Logging Requirements Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/logging-requirements-policy/#d.en.90949)[Password Management Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/password-management-policy/)[Patch Management Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/patch-management-policy/)[Software Development Life Cycle Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/secure-software-development-life-cycle-policy/)[Software Development Life Cycle Procedure](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/secure-software-development-life-cycle-procedure/)[Server Certificate Security Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/server-certificate-security-policy/)[Systems Hardening Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/systems-hardening-policy/)[Web Application IT Security Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/web-application-security-policy/)

## Implementation Information

| Review Frequency: | Annual |
|---|---|
| Responsible Person: | Director, Applications Security |
| Approved By: | CISO |
| Approval Date: | July 31, 2019 |

## Revision History

| Version: | Date: | Description: |
| 1.0 | 07/31/2019 | Initial document |
| 08/17/2020 | Review, no changes | |
| 1.1 | 08/10/2022 | Updated links |
| 1.2 | 10/06/2023 | Updated procedure |