# Key Results

The following four results were selected from the larger automated analysis because they represent important and high-impact risks for the dashcam missing-child search system. The selected results cover missed detections, false positive harm, unequal model performance, and misuse of the search capability.

## Result 1: Relevant Sighting Is Missed or Delayed

### Stakeholder

Missing child

### Goal / Value

Be located and returned to safety as quickly as possible.

### Loss

Searches fail to surface relevant sightings or surface them too slowly, delaying investigators and reducing the chance of timely recovery.

### Requirement

Relevant sightings of the missing child are made available to authorized search coordinators within an operationally useful time window so that perishable leads can be followed before they expire.

### Assumptions

- **ASM1:** Dashcam-equipped vehicles pass through relevant search areas often enough to create opportunities to observe the missing child.
- **ASM2:** When the child appears in dashcam footage, the captured image or video contains sufficient visual information for either automated detection or later human review.
- **ASM3:** Communication connectivity becomes available often enough for candidate sightings to reach investigators while the information is still useful.
- **ASM4:** Reference images and case information provided by investigators correspond to the correct missing child and are suitable for comparison.

### Specifications

- **SPEC1:** When the ML component identifies a potential match, the software records the sighting as a candidate and associates it with the available capture time, location, and supporting media.
- **SPEC2:** The software preserves candidate sightings that cannot immediately be delivered and retries delivery when communication becomes available.
- **SPEC3:** The software exposes delivery status so operators can determine whether a candidate sighting has reached authorized investigators.
- **SPEC4:** The software distinguishes candidate sightings from confirmed sightings so that delayed or uncertain detections are not presented as verified results.


## Result 2: False Positive Leads to Harmful Action

### Stakeholder

Missing child and people captured in dashcam footage

### Goal / Value

Avoid wrongful identification, unnecessary investigation, public exposure, detention, or other harm caused by incorrect automated matches.

### Loss

A person who is not the missing child is treated as a confirmed sighting, potentially leading to wrongful stops, public exposure, emotional distress, or unnecessary investigative action.

### Requirement

People who do not match the missing child are not treated as confirmed sightings solely because of automated person-recognition outputs. Actions that may affect a person's liberty or privacy require independent human verification.

### Assumptions

- **ASM1:** Authorized human reviewers are available to examine candidate sightings before actions are taken based on them.
- **ASM2:** Candidate sightings include enough visual and contextual evidence for a reviewer to reasonably assess whether the person matches the missing child.
- **ASM3:** Investigators follow operational procedures that require verification before treating a candidate as confirmed.

### Specifications

- **SPEC1:** Every automated person-recognition output is labeled as a candidate sighting rather than a confirmed sighting.
- **SPEC2:** The software does not automatically promote an ML-generated candidate to confirmed status.
- **SPEC3:** The software requires an explicit human verification action before a candidate can be marked confirmed or used to trigger consequential external actions.
- **SPEC4:** The software presents the supporting image or video, available location and time information, and the model output to the reviewer before confirmation.


## Result 3: Unequal Detection Performance Across Groups

### Stakeholder

Non-profit child-safety organization and missing children

### Goal / Value

Provide reliable and equitable search support across different demographic groups and deployment conditions.

### Loss

The system systematically misses or under-reports appearances of missing children from particular demographic groups or deployment contexts, reducing their chances of timely recovery and creating unequal service.

### Requirement

Detection and reporting outcomes do not exhibit persistent, substantial disparities across relevant demographic groups or deployment contexts, and significant performance gaps are detectable so they can be investigated and addressed.

### Assumptions

- **ASM1:** Evaluation and review data contain enough information to compare model outcomes across relevant demographic groups and deployment contexts.
- **ASM2:** Human-reviewed outcomes are available for a sufficient sample of candidate sightings to estimate true and false detections.
- **ASM3:** Deployment metadata such as device class, region, lighting conditions, or image quality are available for analysis.
- **ASM4:** The organization defines what level of performance difference is large enough to require investigation.

### Specifications

- **SPEC1:** The software records model version, prediction outcome, relevant deployment context, and review outcome for candidate sightings.
- **SPEC2:** The software computes performance measures across relevant groups and contexts using reviewed outcomes.
- **SPEC3:** The software flags substantial or persistent performance differences for operator review.
- **SPEC4:** The software allows operators to identify which model versions, groups, or deployment contexts are associated with observed performance disparities.


## Result 4: Misuse of Search Capability for Surveillance

### Stakeholder

Non-profit child-safety organization, missing children, families, and members of the public

### Goal / Value

Ensure the system is used only for legitimate missing-child searches and prevent the search capability from becoming a general-purpose tracking or surveillance tool.

### Loss

Malicious actors or unintended users misuse the system to track, surveil, stalk, or otherwise harm children, families, or members of the public.

### Requirement

Search initiation, access to identifying footage, and receipt of search results are limited to authorized participants in active missing-child cases. Unrelated third parties and the public cannot initiate searches or obtain identifying search outputs.

### Assumptions

- **ASM1:** An authoritative list of authorized participants exists for each active missing-child case.
- **ASM2:** Case status is maintained by trusted organizational or investigative personnel and accurately indicates whether a case is active.
- **ASM3:** Authorized participants use identifiable credentials that can be associated with their case role.
- **ASM4:** Organizations revoke or update participant access when roles or case status change.

### Specifications

- **SPEC1:** The software checks that a requester is authenticated and authorized for the specific active case before allowing search initiation or access to identifying results.
- **SPEC2:** The software denies search initiation and identifying-data access when the case is inactive or the requester is not an authorized participant.
- **SPEC3:** The software restricts each authorized role to the minimum search and data-access capabilities needed for that role.
- **SPEC4:** The software records search initiation, access to identifying footage, and delivery of search results in an auditable history associated with the requesting participant and case.