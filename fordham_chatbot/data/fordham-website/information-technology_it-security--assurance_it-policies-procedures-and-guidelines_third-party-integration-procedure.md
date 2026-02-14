https://www.fordham.edu/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/third-party-integration-procedure

# Third-Party Integration Procedure

## Version 1.2

**For Students, Faculty, Staff, Guests, Alumni**

## Purpose

The purpose of this procedure is to ensure third-party integration contracts and Service Level Agreements (SLA) follow the University's requirements. These procedures assist in adherence to the [Third-Party Integration Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/third-party-engagement-policy/).

## Scope

This IT document, and all policies referenced herein, shall apply to all members of the University community, including faculty, students, administrative officials, staff, alumni, authorized guests, delegates, and independent contractors (the “User(s)” or “you”) who use, access, or otherwise employ, locally or remotely, the University’s IT Resources, whether individually controlled, shared, stand-alone, or networked.

## Procedure Statement

When using third-party integrations, arrange that:

- Initial data loads typically performed via SFTP, SSH, or HTTPS require PGP or GPG data encryption before transferring using 4096-bit or greater keys.
- Data integrations are performed via APIs and messaging queues, not by flat-file transfers.
- Third-parties demonstrate they have a formal, documented, and automated process for granting and revoking access to all systems that process or store Fordham Protected Data or Fordham Sensitive Data.
- Third-party User access rights are limited to a need-to-know basis that permits access only to the IT Resources required to perform their duties.
- Third-parties assign unique User IDs, not to be shared with any other individuals when handling Fordham Protected Data or Fordham Sensitive Data.
- Authenticators used in multi-factor authentication (MFA) be stored securely.
- Third-parties maintain an IT Resources access audit and annually make it available to the University either upon request or as an automated log transfer. Be sure the audit includes:
- System security events
- Events that result in the access, modification, or deletion of IT Resources that process or store University data
- A record of the following information for each event:
- Identity of the user/subject,
- Type of event,
- Date and time,
- Source (e.g., email, SFTP record),
- Detection of unauthorized access, and
- Outcome (e.g., success, failure) associated with the event.

- Read-only audit logs are protected from unauthorized access.

- Upon the termination of any third-party engagement, revoke User access immediately.
- Third-party User access is revoked if a job role change eliminates the need to access University's IT Resources.

## Definitions

**GNU Privacy Guard (GPG, also GnuPG)** is a free encryption software compliant with the OpenPGP ([RFC4880](http://www.ietf.org/rfc/rfc4880.txt)) standard.

**IT Resources** include computing, networking, communications, application, telecommunications systems, infrastructure, hardware, software, data, databases, personnel, procedures, physical facilities, cloud-based vendors, Software as a Service (SaaS) vendors, and any related materials and services.

**PGP encryption (Pretty Good Privacy encryption) **is a data encryption program that gives cryptographic privacy and authentication for online communication. It is often used to encrypt and decrypt texts, email, and files to increase email security.

## Related Policies and Procedures

[Data Classification Guidelines](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/data-classification-guidelines/)[Data Classification Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/data-classification-and-protection-policy/)[Data at Rest Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/data-at-rest-policy/)[Data in Transit Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/data-in-transit-policy/)[Third-Party Engagement Policy](/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/third-party-engagement-policy/#d.en.90829)

## Implementation Information

| Review Frequency: | Triennial |
|---|---|
| Responsible Person: | Senior Director of IT Security and Assurance |
| Approved By: | CISO |
| Approval Date: | November 25, 2019 |

## Revision History

| Version: | Date: | Description: |
|---|---|---|
| 1.0 | 11/25/2019 | Initial document |
| 1.1 | 12/04/2020 | Updates to the purpose and procedure statement |
| 1.2 | 08/07/2023 | Updated procedure statement |