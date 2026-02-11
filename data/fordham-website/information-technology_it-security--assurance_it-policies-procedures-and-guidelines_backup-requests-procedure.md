https://www.fordham.edu/information-technology/it-security--assurance/it-policies-procedures-and-guidelines/backup-requests-procedure

# Backup Requests Procedure

## Version 1.0

**For Students, Faculty, Staff, Guests, Alumni**

## Purpose

The purpose of this procedure is to describe how to request backups on Fordham University's Office of Technology owned and managed IT Resources.

## Scope

This IT document and all policies referenced herein shall apply to all members of the University community, including faculty, students, administrators, staff, alumni, authorized guests, delegates, and independent contractors (the "User(s)" or "you") who use, access, or otherwise employ, locally or remotely, the University's IT Resources, whether individually controlled, shared, stand-alone, or networked.

## Procedure

- All requests for Backups can be submitted through the Fordham IT Service Portal using the backup request form in Service Now.
- Access the
[Tech Help Portal](https://fordham.service-now.com/sp)via fordham.edu - Select
[Service Catalog](https://fordham.service-now.com/sp?id=sc_home&catalog_id=e0d08b13c3330100c8b837659bba8fb4) - Select
**IT Internal**from the Service Catalog Categories menu - Select the
**Backup Request/Decommission form**option

- Access the
- The default standard retention (90 days) is applied to all backups unless a specific request is made.
- All Backup Requests that do not adhere to the default standard retention must indicate the technical requirements, including:
- Name of the IT Resources for the backup is requested,
- The length of time the data will be retained,
- Location of the data, including drive or file paths, to be included. Alternatively, Users can request the entire IT Resource to be included,
- Frequency and schedule,
- Any special requirements (regulatory or otherwise).

- The following types of backups can be requested:
- System state backups are requested automatically for systems maintained by the Office of Information Technology when the servers are created and follow the default standard retention. If a specific system requires a different schedule due to special Recovery Point Objective (RPO) or Recovery Time Objective (RTO) requirements, the Application Owner, Database Administrator, or Business Analyst with knowledge of the system must submit a request to modify the schedule.
- Record retention backups are requested to adhere to the
[Records Retention and Disposal Policy](https://www.fordham.edu/info/21366/policies/2785/records_retention_and_disposal_policy). Only data covered by the policy should be included in the backup. The Application owner, Database Administrator, or Business Analyst with system knowledge must submit the request. - Business or research backups are requested for all other purposes. Such requests should not exceed the requirements of the
[Records Retention and Disposal Policy](https://www.fordham.edu/info/21366/policies/2785/records_retention_and_disposal_policy), where applicable. The request must be submitted by the Application Owner, Database Administrator, Business Analyst, or Business Partner with knowledge of the system.

- If the requirement for a specific backup exceeds the
[Records Retention and Disposal Policy](https://www.fordham.edu/info/21366/policies/2785/records_retention_and_disposal_policy)__,__the requestormust have the prior written approval of the Office of Legal Counsel before submitting the request, which must be attached to the Service Now ticket. - The DevOps Systems group will implement all backup requests based on requirements detailed in the Service Now ticket for all instances where they are the System Owner. Once implemented, the relevant Service Now ticket will be closed.
- The DevOps Systems group shall maintain catalogs of all completed backups for later review. These catalogs may be maintained within the software facilitating the backup or separately when such systems are no longer available due to age.
- When a system is requested to leave service or be decommissioned, the data will be retained by the then-current backup requests. No special final backup of a system will be taken. If there are special circumstances that require data to be retained longer, the Application Owner must submit a backup request separately detailing such requirements.

## Definitions

**Application Owner** is the individual or group responsible for ensuring all the services that comprise an application accomplish the specified objective or set of user requirements. If a third party provides these services, the Application Owner is responsible for maintaining the relationships with the third party.

**Backup **is saving or copying information onto digital storage media.

**IT Resources** include computing, networking, communications, application, telecommunications systems, infrastructure, hardware, software, data, databases, personnel, procedures, physical facilities, cloud-based vendors, Software as a Service (SaaS) vendors, and related materials and services.

**Recovery Point Objective** (RPO) is the maximum acceptable amount of data loss measured in time. It is the age of the files or data in backup storage required to resume normal operations if a computer system or network failure occurs.

**Recovery Time Objective** (RTO) is the maximum desired length of time allowed between an unexpected failure or disaster and the resumption of normal operations and service levels. The RTO defines the point in time after a failure or disaster at which the consequences of the interruption become unacceptable.

**Restore/restoration **is performed to return data that has been lost, stolen, or damaged to its original condition or to move data to a new location.

**System Owner** is the individual or group responsible for the procurement, development, integration, modification, operation, maintenance, and retirement of the server, operating system, or other elements that support an Application Owner providing services. The System Owner provides the technical infrastructure for system state and data retention backups. If a third party provides these services, the System Owner is responsible for maintaining the relationship with the third party providing the service.

## Related Policies and Procedures

## Implementation Information

| Review Frequency: | Triennial |
|---|---|
| Responsible Person: | Director of Platform Services |
| Approved By: | CISO and CIO |
| Approval Date: | November 30, 2023 |

## Revision History

| Version | Date | Description |
|---|---|---|
| 1.0 | 11/30/2023 | Initial document |