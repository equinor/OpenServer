# <Title of project/initiative>

`This repository is accessible to all users in the github.com/equinor organisation. Please do not expose any confidential information in the architecture contract or any other files in this repository. (For guidance use IT governance, for TDI projects - R&T governance.`

- **Leading advisor** (primary contact): Unknown
- **EITA architect** (primary contact): Unknown

# Project and Leading advisors summary

Use `R` for `recommend` or `NR` for `Not Recommended` to visualize the “state” of the issues raised.

| Responsible      | Content                                                   | Result (Recommend-R or Not Recommended-NR) | Comments      |
|------------------|-----------------------------------------------------------|--------------------------------------------|---------------|
| EITA             | Aligned with BA strategy                                  | Blank                                      | Comments here |
| EITA             | Aligned with (or develop) TO-BE architecture for the area | Blank                                      | Comments here |
| Leading advisors | Comply with technical direction                           | Blank                                      | Comments here |
| Leading advisors | IT Technology                                             | Blank                                      | Comments here |
| Leading advisors | Information Management                                    | Blank                                      | Comments here |


# Meeting log

- DD.MM.YYYY - Document participants and type of meeting.
- DD.MM.YYYY - Document participants and type of meeting.

## Next meeting

DD.MM.YYYY

## Discussions

Discussion from meetings. Address the topic and what was discussed / commented. See the [wiki](https://wiki.equinor.com/wiki/index.php/Architecture_Contract/Architecture_Topics) for information, and the topics/self-assessment page specifically for common topics to discuss and fill in below.

| Area           | Topic                 | Comment                |
|----------------|-----------------------|------------------------|
| Cyber Security | Authentication        | Comments to the topic  |
| Ownership      | DevOps team, size etc | Comments to the topic  |
| ...            | ...                   | ...                    |
| Other areas    | Other topics          | Comments to the topics |


---
TODO Before starting self assessment, take a look at https://wiki.equinor.com/wiki/index.php/Architecture_Contract/Architecture_Topics and look for updates since last version of this .md file.
---

# Overview

## Main functionality

## Software Architecture

## Security and information management

## Self assessment

### General
1. **Which business area is the solution meant for?**

2. **Who are the users?**

3. **Application description (brief)**

4. **Main technologies (programming languages, frameworks, run-time environments etc)**

5. **Where will the software be hosted?**

6. **Link to architecture diagrams (preferably C4 Model for software architecture)**

7. **How has EITA been involved in ensuring alignment with the strategy for the business area?**

### Software Development & Software Architecture

1. **Does the software use any technology components not registered as Now/green (or not listed at all) in https://techlifecycle.equinor.com? If yes, please list them.**

2. **Does the application expose relevant data/functionality only using approved API mechanisms, as listed in https://techlifecycle.equinor.com ?**

3. **If you are exposing APIs, have you adapted to the principles in the Equinor API Strategy?**

4. **Have you evaluated how the application should handle personal data, with GDPR regulations in mind? This includes logging of information that can identify a person, like name name, userID, email, etc.**

5. **Is the software subject to export control?**

6. **TR1621, 2.8.1: "All software developed by/for Equinor shall be made opensource, unless IP rights prevents this or there are unacceptable risks." Have you made your software open source? If not, please explain why.**

7. **If you are considering bying (or already have bought) software tools, frameworks, libraries; Have you evaluated open source alternatives?**

8. **If you are considering consuming services based on proprietary software; Have you evaluated alternative services based on open source software?**

9. **Have all team members participated on software developer onboarding within the last 12 months?**

10. **Does the team follow a documented Software Development Lifecycle Process? Describe very briefly.**

11. **Do you do auditable code reviews for at least the major/central parts of the code?**

12. **Do you deliver your software in iterations, with short feedback loops?**

13. **Do you have a process for continuous improvement (e.g. by regular retrospectives)?**

14. **Do the software developers have direct contact with the users of the software?**

15. **Do you have an automated CI/CD pipeline?**

16. **Please describe (using keywords) how the software is being tested?**

17. **Do you have automated tests, run as part of your CI/CD pipeline?**

18. **Have you assessed the technical debt in the software? How will you handle it?**

19. **If your application contains a GUI, are you aligning your design with the Equinor Design System: https://eds.equinor.com**

### Data & Information Architecture

1. **Where is data in your application coming from?**

2. **How is the data flowing into your application?**

3. **How will other applications consume data from your application?**

4. **Must your application be kept in sync with other applications (where same or related data appears multiple places? If yes, how are they kept in sync (e.g. Event-based? Sync-based?)**

5. **Is data in your application immutable, i.e. data is never updated or deleted? Are there any special requirements regarding retention?**

6. **Is your application considered to be "systems of records" for all data or a subset of data in the application? I.e. It holds the source of truth. If there is a deviation between another system and system of record, the value in the system of record is by definition the correct one.**

7. **Is your application considered to be a "derived data system", i.e. data in your application is the result of taking some existing data from another system and transforming or processing it in some way. If you lose the derived data in your application, can you easily re-create from the original sources?**

8. **If we want to exit the application, but keep data usable other places - how do you plan doing that?**

9. **Is your data named / structured / modeled according to established international or national open standards?**

### Security and information management

1. **Who is the information owner for the software/application?**

2. **What is the classification of the information handled by the software (open, internal, restricted, confidential)?**

3. **Have you assessed how the information classification impact the security in the software?**

4. **Has a Security Risk Assessment been performed (ordered in Services@Equinor as "Information Risk Assessment)?**

5. **If you will move data into the cloud, in many cases a Legal Risk Assessment must be performed. See KB0042661 for more information. Have you done this, if relevant?**

6. **Will you (or have you) ordered a penetration test?**

### Operations

1. **Which team / department will have the operational responsibility for the software?**

2. **Has the RunBook been created?**

3. **Has service design been done (LM of the department with operational responsibility is responsible)?**

4. **Do you have any operational monitoring of the application?**

5. **What have you done to ensure reliability and resilience in the software?**

6. **What have you done to make it as easy and efficient as possible to operate the solution (reducing Total Cost of Ownership)?**

#### For procured software:

1. **What kind of support & maintenance agreement do you have with vendor (if procured software)?**

2. **How often will you get updates?**

3. **Are the vendor committed to follow the lifecycle on components they are depending on, such as Microsoft SQL server, Microsoft Windows etc.?**

### Other

Are there other topics or issues you would like to discuss? Please list them.

1. ...
