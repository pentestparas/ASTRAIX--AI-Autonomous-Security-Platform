OWASP API Security Project | OWASP Foundation OWASP API Security Project

# 

 Check out the new OWASP API Security Top 10 2023 ! What is API Security?

## 

 A foundational element of innovation in today’s app-driven world is the API.
From banks, retail and transportation to IoT, autonomous vehicles and smart
cities, APIs are a critical part of modern mobile, SaaS and web applications and
can be found in customer-facing, partner-facing and internal applications. By
nature, APIs expose application logic and sensitive data such as Personally
Identifiable Information (PII) and because of this have increasingly become a
target for attackers. Without secure APIs, rapid innovation would be impossible.

 API Security focuses on strategies and solutions to understand and mitigate the
unique vulnerabilities and security risks of Application Programming Interfaces
(APIs). API Security Top 10 2023

## 

 Here is a sneak peek of the 2023 version:

- 

 API1:2023 - Broken Object Level Authorization

 APIs tend to expose endpoints that handle object identifiers, creating a wide
attack surface of Object Level Access Control issues. Object level
authorization checks should be considered in every function that accesses a
data source using an ID from the user. Continue reading .
- 

 API2:2023 - Broken Authentication

 Authentication mechanisms are often implemented incorrectly, allowing
attackers to compromise authentication tokens or to exploit implementation
flaws to assume other user’s identities temporarily or permanently.
Compromising a system’s ability to identify the client/user, compromises API
security overall. Continue reading .
- 

 API3:2023 - Broken Object Property Level Authorization

 This category combines API3:2019 Excessive Data Exposure and API6:2019 - Mass Assignment , focusing on the root cause: the lack
of or improper authorization validation at the object property level. This
leads to information exposure or manipulation by unauthorized parties. Continue reading .
- 

 API4:2023 - Unrestricted Resource Consumption

 Satisfying API requests requires resources such as network bandwidth, CPU,
memory, and storage. Other resources such as emails/SMS/phone calls or
biometrics validation are made available by service providers via API
integrations, and paid for per request. Successful attacks can lead to Denial
of Service or an increase of operational costs. Continue reading .
- 

 API5:2023 - Broken Function Level Authorization

 Complex access control policies with different hierarchies, groups, and roles,
and an unclear separation between administrative and regular functions, tend
to lead to authorization flaws. By exploiting these issues, attackers can gain
access to other users’ resources and/or administrative functions. Continue
reading .
- 

 API6:2023 - Unrestricted Access to Sensitive Business Flows

 APIs vulnerable to this risk expose a business flow - such as buying a ticket,
or posting a comment - without compensating for how the functionality could
harm the business if used excessively in an automated manner. This doesn’t
necessarily come from implementation bugs. Continue reading .
- 

 API7:2023 - Server Side Request Forgery

 Server-Side Request Forgery (SSRF) flaws can occur when an API is fetching a
remote resource without validating the user-supplied URI. This enables an
attacker to coerce the application to send a crafted request to an unexpected
destination, even when protected by a firewall or a VPN. Continue
reading .
- 

 API8:2023 - Security Misconfiguration

 APIs and the systems supporting them typically contain complex configurations,
meant to make the APIs more customizable. Software and DevOps engineers can
miss these configurations, or don’t follow security best practices when it
comes to configuration, opening the door for different types of attacks. Continue reading .
- 

 API9:2023 - Improper Inventory Management

 APIs tend to expose more endpoints than traditional web applications, making
proper and updated documentation highly important. A proper inventory of hosts
and deployed API versions also are important to mitigate issues such as
deprecated API versions and exposed debug endpoints. Continue
reading .
- 

 API10:2023 - Unsafe Consumption of APIs

 Developers tend to trust data received from third-party APIs more than user
input, and so tend to adopt weaker security standards. In order to compromise
APIs, attackers go after integrated third-party services instead of trying to
compromise the target API directly. Continue reading . Licensing

## 

 The OWASP API Security Project documents are free to use!

 The OWASP API Security Project is licensed under the Creative Commons
Attribution-ShareAlike 4.0 license , so you can copy, distribute and
transmit the work, and you can adapt it, and use it commercially, but all
provided that you attribute the work and if you alter, transform, or build upon
this work, you may distribute the resulting work only under the same or similar
license to this one. Founders

## 

- Erez Yalon
- Inon Shkedy Leaders

## 

- Erez Yalon
- Inon Shkedy
- Paulo Silva 2023 Sponsors

## 

 2023 Contributors

## 

 247arjun, abunuwas, Alissa Knight, Arik Atar, aymenfurter, Corey J. Ball, cyn8,
d0znpp, Dan Gordon, donge, Dor Tumarkin, faizzaidi, gavjl, guybensimhon, Inês
Martins, Isabelle Mauny, Ivan Novikov, jmanico, Juan Pablo, k7jto, LaurentCB,
llegaz, Maxim Zavodchik, MrPRogers, planetlevel, rahulk22, Roey Eliyahu, Roshan
Piyush, securitylevelup, sudeshgadewar123, Tatsuya-hasegawa, tebbers, vanderaj,
wenz, xplo1t-sec, Yaniv Balmas, ynvb 2019 Contributors

## 

 007divyachawla, Abid Khan, Adam Fisher, anotherik, bkimminich, caseysoftware,
Chris Westphal, dsopas, DSotnikov, emilva, ErezYalon, flascelles, Guillaume
Benats, IgorSasovets, Inonshk, JonnySchnittger, jmanico, jmdx, Keith Casey,
kozmic, LauraRosePorter, Matthieu Estrade, nathanawmk, PauloASilva, pentagramz,
philippederyck, pleothaud, r00ter, Raj kumar, Sagar Popat, Stephen Gates,
thomaskonrad, xycloops123, Raphael Hagi, Eduardo Bellis, Bruno Barbosa Google Group

## 

 Join the discussion on the OWASP API Security Project Google group .

 This is the best place to introduce yourself, ask questions, suggest and discuss
any topic that is relevant to the project. GitHub Discussions

## 

 You can also use GitHub Discussions as a place to connect with other community
members, asking questions or sharing ideas. GitHub

## 

 The project is maintained in the OWASP API Security Project repo .

 The latest changes are under the
```
 develop branch .

 Feel free to open or solve an issue .

 Ready to contribute directly into the repo? Great! Just make sure you read the How to Contribute guide .

- 

 Jun 28th, 2024

 OWASP API Security Project - Past Present and Future @ OWASP Global AppSec
Lisbon 2024 ( YouTube )
- 

 Jun 3rd, 2024

 OWASP API Security Top 10 2023 French translation release.
- 

 Jun 5th, 2023

 OWASP API Security Top 10 2023 stable version was publicly
released.
- 

 Feb 14, 2023

 OWASP API Security Top 10 2023 Release Candidate is
now available.
- 

 Aug 30, 2022

 OWASP API Security Top 10 2022 call for data is open.
- 

 Oct 30, 2020

 GraphQL Cheat Sheet release.
A truly community effort whose log and contributors list are available at
GitHub .
- 

 Apr 4, 2020

 OWASP API Security Top 10 2019 pt-PT translation release.
- 

 Mar 27, 2020

 OWASP API Security Top 10 2019 pt-BR translation release.
- 

 Dec 26, 2019

 OWASP API Security Top 10 2019 stable version release.
- 

 Sep 30, 2019

 The RC of API Security Top-10 List was published during OWASP Global AppSec
Amsterdam ( slide deck )
- 

 Sep 13, 2019

 The RC of API Security Top-10 List was published during OWASP Global AppSec
DC ( slide deck )
- 

 May 30, 2019

 The API Security Project was Kicked-Off during OWASP Global AppSec Tel
Aviv ( slide deck ) Planned Projects

## 

- API Security Top 10
- API Security Cheat Sheet
- crAPI - C ompletely R idiculous API , an intentionally vulnerable API
project) Roadmap

## 

 OWASP API Security Top 10 2023

## 

- 

 Bahasa (Indonesian)

 Faiz Ahmed Zaidi
- 

 French

 Aurélien Troncy , Laurent Legaz
- 

 Persian

 Alireza Mostame , Maryam Javadi Hoseini , Mohammad Reza Ismaeli Taba , RNPG
- 

 Português (Portugal)

 Rui Silva OWASP API Security Top 10 2019

## 

- 

 Arabic (also available in PDF , ODT )

 Malek Aldossary , Sabri Hassanyah , Mostafa Alaqsm , Fahad Alduraibi , Thamer Alshammeri , Mohammed Alsuhaymi
- 

 French (also available in PDF , ODT )

 Fred , Laurent Legaz
- 

 German (also available in PDF , ODT )

 Moritz Gruber , Nick Lorenz , Steffen Thamm , Tim B.
- 

 Greek ( PDF , ODT )

 Athanasios Emmanouilidis , Apostolos Giannakidis
- 

 Persian (also available in PDF , ODT )

 Alireza Mostame , Mohammad Reza Ismaeli Taba , Amirmahdi Nowbakht , RNPG
- 

 Portuguese (Brazil) (also available in PDF , ODT )

 Raphael Hagi , Eduardo Bellis , Bruno Barbosa
- 

 Portuguese (Portugal) (also available in PDF , ODT )

 Paulo A. Silva , Rui Silva
- 

 Russian (also available in PDF , ODT )

 Eugene Rojavski , act1on3 , keni0k Watch Star The OWASP ® Foundation works to improve the security of software through its community-led open source software projects, 
 hundreds of chapters worldwide, tens of thousands of members, and by hosting local and global conferences. API Security Information

### 

 Builders Breakers Defenders

 Downloads or Social Links

### 

- API Security Top 10 2023
- API Security Top 10 2019 ( PDF )
- GraphQL Cheat Sheet
- GitHub Discussions
- Mailing List Code Repository

### 

- GitHub Leaders

### 

- Erez Yalon
- Inon Shkedy
- Paulo Silva Upcoming OWASP Global Events

###