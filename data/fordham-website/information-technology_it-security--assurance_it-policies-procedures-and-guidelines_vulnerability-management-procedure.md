https://www.fordham.edu/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/vulnerability-management-procedure

# Vulnerability Management Procedure

## Version 2.1

**For Students, Faculty, Staff, Guests**

## Purpose

The purpose of this procedure is to delineate the steps involved in IT vulnerability management in accordance with the [Vulnerability Management Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/vulnerability-management-policy/#d.en.90893). It ensures the utilization of suitable tools and methodologies to evaluate vulnerabilities within systems or applications and facilitate remediation.

## Scope

This IT document and all policies referenced herein shall apply to all members of the University community, including faculty, students, administrators, staff, authorized guests, delegates, and independent contractors (the “User(s)” or “you”) who use, access, or otherwise employ, locally or remotely, the University’s IT Resources, whether individually controlled, shared, stand-alone, or networked.

## Procedure Steps

The steps in the vulnerability management procedure ensure a systematic approach to identifying, prioritizing, planning for, addressing, and validating the resolution of vulnerabilities within IT systems and applications.

**Discovery Phase:**Identify vulnerabilities present within IT Resources.**Prioritization Phase:**Discovered vulnerabilities and assets are reviewed, prioritized, and assessed using results from technical and risk reports.**Planning Phase:**Devise comprehensive mitigation strategies and action plans to address identified vulnerabilities.**Remediation Phase**: Implement necessary measures to address and rectify vulnerabilities identified during the discovery phase.**Validation Phase:**Conduct subsequent analysis to determine the effectiveness of the remediation measures deployed.

### Discovery Phase

Utilize tools such as [BitSight](https://www.bitsight.com/), [Burp Suite](https://portswigger.net/burp), [Invicti (formerly Netsparker)](https://www.invicti.com/), [Nmap](https://nmap.org/), [Qualys](https://www.qualys.com/), and [WPScan](https://wpscan.com/) to identify vulnerabilities on IT Resources.[1](#_ftn1)

### Prioritization Phase

Application and system owners review and prioritize vulnerabilities based on severity levels and risk assessments. Prioritization Criteria:

- Address confirmed severity levels 5, 4, or 3 findings in Qualys.
- Prioritize vulnerabilities with a Qualys TruRisk Score of 700 or higher (High or Severe).
- Attend to BitSight Bad Grade, Asset Importance High/Critical, and Finding Severity Material/Severe.
- Address all severity levels findings in Invicti (formerly Netsparker) (Critical, High, Medium).
- Include content security policy configurations, application header configurations, or certificate configuration findings in the prioritization process.
- Seek guidance from Information Security and Assurance in case of conflicting severity levels.

### Planning Phase

Remediation for the vulnerability findings should be mitigated and validated within the following time frame from initial discovery (i.e., first detected date of vulnerability on respective IT Resources):

- Within 30 Days
- All BitSight findings graded as Bad
- Qualys confirmed severity levels 5 and 4
- Confirmed Qualys severity levels 5, 4, and 3 on all systems within the PCI Network
- Invicti (formerly Netsparker) Critical and High Severity Levels

- Within 60 Days
- Qualys confirmed Severity Level 3
- Remaining Invicti (formerly Netsparker) Medium and Low severity levels

- The ISA may identify findings that are not directly in line with the assessment tools mentioned above and may need to be addressed outside the noted days mentioned.

### Remediation Phase

System and application owners must undertake one or more of the following, including but not limited to:

- Mitigating controls with ISA approval.
- Patches deployment.
- Configuration changes deployment.
- System upgrades.
- Removal/discontinuation of IT Resources usage.

### Validation Phase

- Verify the effectiveness of remediation efforts through thorough analysis and validation.
- Ensure that vulnerabilities are successfully addressed and no longer pose a threat.
- Address any discrepancies between remediation actions and validation results.
- Escalate unresolved issues or false positives to the Information Security and Assurance team for further investigation and resolution.
- Verify the vulnerability no longer exists based on finding the source (e.g., assessment tool, ad hoc finding).
- If remediation has taken place, and the change is not reflected in a validation scan or deemed not applicable (e.g., if mitigating controls were implemented, vulnerability is a false positive), the application or system owner is responsible for letting the Information Security and Assurance know via email at
[[email protected]](/cdn-cgi/l/email-protection#a8c1c6cec7dbcdcbe8cec7daccc0c9c586cdccdd)

1Depending on the nature of an OS or application deployed, Information Security and Assurance may leverage alternative assessment tools or methodologies to determine vulnerabilities.

## Definitions

**IT Resources** include computing, networking, communications, application, and telecommunications systems, infrastructure, hardware, software, data, databases, personnel, procedures, physical facilities, cloud-based vendors, Software as a Service (SaaS) vendors, and any related materials and services.

A **patch** is a software update comprised of code inserted (i.e., patched) into the code of an executable program. Typically, a patch is installed into an existing software program. Patches are often temporary fixes between full releases of a software package. Patches include, but are not limited to, the following:

- Upgrading software
- Fixing a software bug
- Installing new drivers
- Addressing security vulnerabilities
- Addressing software stability issues

**Remediation **is an effort that resolves or mitigates a discovered vulnerability.

**Vulnerability** is a flaw or weakness in system security procedures, design, implementation, or internal controls that could be exercised (accidentally triggered or intentionally exploited) and result in a security breach or a violation of the system’s security policy.

**Vulnerability management** is the practice of identifying, classifying, remediating, and mitigating vulnerabilities.

### Related Policies and Procedures

## Implementation Information

| Review Frequency: | Annual |
|---|---|
| Responsible Person: | Senior Director of IT Security and Assurance |
| Approved By: | CISO |
| Approval Date: | March 25, 2019 |

## Revision History

| Version: | Date: | Description: |
|---|---|---|
| 1.0 | 01/08/2018 | Initial document |
| 1.1 | 03/25/2019 | Procedure updates |
| 05/08/2020 | Periodic review | |
| 1.2 | 07/26/2021 | Updated statement and removed products no longer in use |
| 1.3 | 08/10/2022 | Updated procedure statement |
| 1.4 | 11/29/2023 | Updated WPScan |
| 2.0 | 03/06/2024 | Updated purpose, scope, procedure |
| 2.1 | 05/21/2024 | Updated Invicti (formerly Netsparker) |