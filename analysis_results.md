# Comprehensive Risk Analysis

This report contains the stakeholder-centered hazard analysis generated with LLM assistance and reviewed as part of a human-in-the-loop workflow.

## 1. Missing child

### Goals

- **G1**: Be located and returned to safety as quickly as possible.
- **G2**: Avoid being wrongly identified or publicly exposed in ways that cause stress, detention, or reputational harm.
- **G3**: Have identifying images and location information kept private except when legitimately needed for the search.
- **G4**: Avoid secondary harms from reuse or prolonged retention of their images or location data (e.g., stalking, exploitation, discrimination).

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Searches fail to surface relevant sightings or do so too slowly, delaying investigators and reducing the chance of timely recovery.

**Requirement (REQ1):** Relevant sightings of the missing child are made available to authorized search coordinators within an operationally useful time window so that perishable leads can be followed before they expire.

**Assumptions (ASM):**

- **ASM1**: Each dashcam that may observe the child is operational and produces capture artifacts that include a synchronized timestamp and geo-location (GPS) metadata accessible to the software for every recorded frame or image.
- **ASM2**: Dashcam-equipped vehicles traverse the missing child's last-known or probable search area frequently enough relative to the case's operational_time_window parameter (i.e., at least one vehicle enters the area within that window) to create opportunities for sightings.
- **ASM3**: Network connectivity (cellular, vehicle-to-cloud, or other upload path) is available often enough and with sufficient bandwidth/latency that a substantial fraction of captured candidate-sighting packages (image + metadata) can be uploaded to the backend within the case's operational_time_window; intermittent outages may occur but are not permanent for the duration of the window.
- **ASM4**: Investigative partners supply reference images and case metadata that correspond to the correct child, including at least one clear frontal face image and any known distinguishing clothing or accessories, with timestamps indicating when the reference images were captured.

**Specifications (SPEC):**

- **SPEC1**: When the onboard ML or rule-based detector flags a potential sighting, the software must create a candidate-sighting record that includes: capture timestamp, GPS coordinates, camera/vehicle identifier, the extracted frame(s) or thumbnail(s), the ML model version, and a confidence score; the record must be explicitly labeled as a candidate sighting (not a confirmed sighting).
- **SPEC2**: For each candidate-sighting record, the software must attempt delivery to the authorized search-coordinator endpoints so that delivery completes within the case's configurable operational_time_window whenever possible. The software must record the time of first transmission attempt and time of successful delivery; if immediate delivery fails, the software must retry with an exponential backoff schedule and, if delivery cannot be completed before the operational_time_window expires, mark the record as delayed and generate a delivery-failure notification (including reason and ETA for next upload) to coordinators using any configured alternate channels (e.g., email/SMS).
- **SPEC3**: Access to candidate sightings and associated metadata must be restricted to authenticated and authorized accounts representing search coordinators; all accesses and sharing actions must be auditable by recording user identity, action type, timestamp, and sighting identifier in an immutable audit log.
- **SPEC4**: The software must group and de-duplicate candidate sightings that fall within configurable spatial and temporal thresholds into aggregated sighting clusters, compute an aggregated score and provenance summary for each cluster (e.g., number of supporting captures, highest individual confidence, time range, and distinct camera IDs), and present clusters to coordinators ordered by a configurable priority function (e.g., recency and maximum confidence).

#### H2 / REQ2

**Related Goal:** G2

**Loss:** People who are not the missing child are treated as confirmed sightings, leading to wrongful stops, public exposure, emotional distress, or other harms to the child and their family.

**Requirement (REQ2):** People who do not match the missing child are not presented to investigators or third parties as confirmed sightings based solely on automated outputs; any reported sighting relied upon for actions that affect the child's liberty or privacy must be corroborated by independent human verification.

**Assumptions (ASM):**

- **ASM1**: Human investigators or designated verifiers will review candidate sightings within a defined maximum review window (e.g., 24 hours) after the software submits them.
- **ASM2**: Source devices (dashcams) include and transmit reliable, machine-readable location and timestamp metadata (e.g., GPS coordinates and UTC timestamp) that are synchronized within a known tolerance (e.g., ±5 seconds) to a global time source.
- **ASM3**: There exists an independent, human-accessible channel for obtaining higher-fidelity or raw evidence (e.g., full-resolution video, multiple frames, eyewitness contact information) from the environment or device owners that verifiers can use to corroborate automated candidate sightings.

**Specifications (SPEC):**

- **SPEC1**: All ML-generated detections must be labeled and stored as 'candidate sighting' in the system; the software must not create, display, or transmit any report marked or implied as a 'confirmed sighting' to investigators, third parties, or external systems based solely on automated outputs.
- **SPEC2**: Before any sighting is elevated from 'candidate' to a state that can trigger actions affecting a person's liberty or privacy (e.g., police stop requests, public alerts, sharing of identifying images), the software must require and record an explicit human verification action: verifier identifier, verification timestamp, and the specific corroborating evidence used.
- **SPEC3**: For each candidate sighting the software must: record and store ML model outputs and provenance (including confidence scores, model version, bounding boxes, and input frames), attach available device metadata (GPS, timestamp), and present these items to the human verifier in a single view; the system must not permit automated confirmation regardless of model confidence.
- **SPEC4**: When sharing candidate sightings with any third party or publishing outside the internal verification workflow, the software must redact or obfuscate personally identifying visual information (e.g., blur faces, remove registration plates) and indicate the item is unverified; only after the recorded human verification step may the system disclose unredacted identifying media or enable operational actions.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Identifying images or location information from dashcam footage are accessed or shared with unauthorized parties, enabling stalking, exploitation, or unwanted media exposure of the child.

**Requirement (REQ3):** Identifying images and location information of the missing child are accessible only to authorized search personnel and designated partner organizations, and are not disclosed to unauthorized individuals or services.

**Assumptions (ASM):**

- **ASM1**: Dashcam devices and backend systems can capture and attach location metadata (e.g., GPS coordinates) and capture timestamps to images/videos at the time of capture, and device clocks or GNSS receivers provide time/position data within known tolerances.
- **ASM2**: Authorized search personnel and designated partner organizations hold and present valid authentication credentials and authorization approvals issued by the coordinating authority, and the authority maintains a current list of authorized accounts and roles.
- **ASM3**: Applicable legal, contractual, and privacy agreements permit the sharing of identifying images and location information with the specified authorized search personnel and partner organizations, and those partners agree to abide by data-handling restrictions.

**Specifications (SPEC):**

- **SPEC1**: The software must enforce authentication and role-based authorization before disclosing any identifying images or location metadata: requests must provide valid multi-factor authentication and the requester’s role must be checked against the case-specific access control list; unauthorized requests must be denied (HTTP 403 or equivalent) and logged.
- **SPEC2**: All identifying images and associated location metadata must be encrypted at rest and in transit; decryption keys must be stored in a managed key store with access controls that only permit key usage for authorized accounts and services after successful authorization checks.
- **SPEC3**: When an ML component flags a candidate sighting, the system must label outputs as 'candidate' (not confirmed), store lower-resolution/blurred preview images for low-tier access, and require manual verification and explicit approval by an authorized investigator before releasing full-resolution identifying images or precise location coordinates to any account that lacks top-tier clearance.
- **SPEC4**: The system must produce immutable audit logs for every access attempt to identifying images or location data (including requester ID, role, case ID, timestamp, requested resource, result), retain those logs for at least 365 days, and generate real-time alerts to administrators on failed authorization attempts or unusual access patterns; the system must allow immediate revocation of access for any authorized account.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Footage containing the child's likeness is retained or repurposed for unrelated uses, creating long-term privacy, safety, or discrimination risks to the child.

**Requirement (REQ4):** Recorded footage or images containing the missing child's likeness are not used for purposes unrelated to the active search and are rendered inaccessible for other uses after the search concludes or as required by applicable retention policies and legal protections.

**Assumptions (ASM):**

- **ASM1**: An authorized case-control signal (e.g., investigator-issued 'case open' and 'case closed' commands, or legal retention directives) will be delivered to the system and correctly identify the relevant missing-child case and responsible authority.
- **ASM2**: Storage endpoints that hold footage (on-device flash, local vehicle storage, cloud buckets, and backups) support programmatic access control changes and deletion or key-revocation operations when requested by the system or by an authorized agent.
- **ASM3**: Investigators or authorized custodial agents supply, at case initiation or via accessible policy registry, the retention duration and permitted uses (including legal exceptions) that apply to footage containing the child's likeness for that jurisdiction.

**Specifications (SPEC):**

- **SPEC1**: When footage or image frames are identified as containing the missing child's likeness (either by ML candidate detection or by human report), the software must store those items in a designated, access-restricted case storage compartment that: (a) is tagged with the case ID and retention metadata, (b) prevents access by other system features (e.g., analytics, model training pipelines, advertising), and (c) requires explicit authorization from an investigator account to remove those access restrictions during the active search.
- **SPEC2**: Upon receipt of an authorized 'case closed' command or upon expiry of the case-specific retention period supplied by investigators/legal directives, the software must render all stored footage/images containing the child's likeness inaccessible for downstream uses by performing one or more of the following programmatic operations supported by the storage endpoint: permanent deletion of files, secure erasure of local copies, and/or cryptographic key destruction that prevents future decryption; the chosen operation must be recorded in an auditable deletion action log.
- **SPEC3**: The software must maintain an immutable audit log for every access, copy, export, ML inference, and deletion action involving footage/images tagged with the child's likeness; each log entry must include timestamp, actor identity (human or service), action type, and the case ID, and the system must provide a verifiable deletion receipt showing which storage endpoints and backup locations were affected when footage is rendered inaccessible.
- **SPEC4**: ML-related workflow: any output produced by automated detection (cropped images, feature vectors, embeddings, match scores) that is derived from footage containing the child's likeness must be handled with the same access restrictions and retention metadata as the original footage; the software must block automatic incorporation of these artifacts into model training, benchmarking, or third-party feature sets unless a documented, investigator-authorized exception is recorded in the audit log.

## 2. Parent or legal guardian

### Goals

- **G1**: Locate the missing child quickly by receiving timely and relevant sightings.
- **G2**: Protect the child's and family's privacy and control over images and location data.
- **G3**: Avoid wrongful identification of people that leads to distress, wasted resources, or legal exposure.
- **G4**: Prevent misuse of images or location data for stalking, harassment, or public exposure.
- **G5**: Avoid unexpected financial, battery, or storage burdens on personal devices that impede participation in the search.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Delays or failures to detect the child in dashcam footage lead to missed opportunities to locate the child and delayed search response.

**Requirement (REQ1):** When the missing child appears in recorded or live dashcam footage, authorized investigators and the reporting parent receive relevant sightings (including timestamps and location) within an acceptable time window to support timely search actions.

**Assumptions (ASM):**

- **ASM1**: Each dashcam or its ingest pipeline embeds accurate UTC timestamps and geolocation (latitude/longitude) in recorded footage metadata, with device clocks synchronized to a trusted time source within +/- 5 seconds.
- **ASM2**: When the missing child appears in footage the child is visible with sufficient image quality for recognition (e.g., face or distinctive clothing visible in at least 3 consecutive frames, resolution and lighting permit human or automated matching).
- **ASM3**: At least one communication path (cellular, Wi‑Fi, or periodic upload via a paired device) becomes available to transmit detection metadata or media to the processing server within the system-configured acceptable time window for the majority (>90%) of incidents, or the dashcam/storage system can buffer data until such a path is available.
- **ASM4**: Reference images and identifying information provided by the reporting parent correspond to the correct child and were captured recently enough that appearance has not changed materially (e.g., within the last 12 months or as specified per case).

**Specifications (SPEC):**

- **SPEC1**: For every candidate sighting the software must record and attach: source dashcam ID, UTC timestamp(s) of the frame(s), GPS coordinates from the source metadata, a clipped video segment or representative frames, and an automated confidence score and bounding box coordinates; these fields must be stored in the case record and be retrievable via API or UI.
- **SPEC2**: The software must attempt delivery of a sighting alert (including timestamp, location, representative media, and confidence) to the reporting parent and all authorized investigators within the system-configured acceptable time window after detection; if delivery is not completed within that window the software must mark the sighting as delayed, enqueue repeated delivery attempts, and record the delivery status and timestamps for each attempt.
- **SPEC3**: Automated detections must be presented as 'candidate sightings' (not confirmed), include model confidence and visual indicators (bounding boxes, sample frames), and provide workflows for an authorized investigator to explicitly confirm or dismiss the candidate; the software must record the investigator's action and timestamp in the case record.
- **SPEC4**: Access to sighting media and metadata must be restricted to authenticated accounts authorized for that missing‑child case (reporting parent and case investigators); every access and every outbound alert delivery attempt must be logged with actor, method, and timestamp for audit and monitoring purposes.

#### H2 / REQ2

**Related Goal:** G3

**Loss:** Automated misidentification causes innocent people to be treated as matches, resulting in false leads, reputational harm, harassment, or wasted investigative resources for the parent and authorities.

**Requirement (REQ2):** People who do not match the missing child are not treated as confirmed sightings or actionable leads solely based on an automated prediction; only human-verified sightings are advanced as confirmed leads to investigators or the public.

**Assumptions (ASM):**

- **ASM1**: At least one authorized human reviewer (parent/legal guardian or designated investigator) is reachable and able to examine candidate sighting reports before any sighting is declared confirmed.
- **ASM2**: Captured images or video for candidate sightings retain sufficient identifiable features (e.g., face not fully occluded, minimal motion blur, and adequate resolution) in a measurable majority of cases so a human reviewer can make an identity determination from the media provided.
- **ASM3**: Communication channels used to deliver human-verified confirmations to investigators, parents, or public authorities (e.g., network connectivity, investigator dashboards, email/SMS gateways) function often enough to permit delivery of verified reports within the operational timeframe for an active missing-child investigation.

**Specifications (SPEC):**

- **SPEC1**: All automated model outputs indicating a potential match must be stored and displayed only as 'candidate sighting' status. The software must not change any candidate sighting to 'confirmed' or forward it to investigators or the public as a confirmed sighting without an explicit human verification action.
- **SPEC2**: The software must require an explicit human verification operation to mark a candidate sighting as confirmed. That operation must record the verifier's identity, role, timestamp, and a mandatory free-text rationale or selection from predefined reasons, and must be immutable in the event timeline.
- **SPEC3**: When presenting candidate sightings to a human reviewer, the software must include: the original reference images, the candidate capture (images/video), the model's confidence score(s), and model-generated salient evidence (e.g., bounding boxes, similarity metrics). The interface must provide reviewer actions to: Confirm, Reject (false positive), or Defer (insufficient information).
- **SPEC4**: The software must restrict dissemination of candidate sightings to internal, authenticated, and authorized accounts only. Notifications to external parties or public channels must be automatically gated so they are sent only after a sighting's status is set to 'confirmed' by a human verifier, and every external notification must include the recorded human-verification metadata and a link to the audit trail.

#### H3 / REQ3

**Related Goal:** G2

**Loss:** Reference photos or dashcam footage are exposed to unauthorized parties, enabling privacy violations, harassment, or downstream misuse of identifying images of the child or family.

**Requirement (REQ3):** Unauthorized parties do not gain access to identifying images, footage, or location information related to the missing child or the reference photos provided by the parent.

**Assumptions (ASM):**

- **ASM1**: Client devices and deployed servers used to upload or store reference photos and dashcam footage provide hardware-backed secure key storage (e.g., TPM or platform keystore) that the software can detect and use.
- **ASM2**: Any third-party cloud or storage provider used by the system enforces role-based access control, supports server-side encryption, and produces access logs for object read/write operations that are available to the software for auditing.
- **ASM3**: Account holders (parents/legal guardians) enable and maintain multi-factor authentication (MFA) on their accounts as instructed, so the software can observe an MFA-enabled flag on the account.

**Specifications (SPEC):**

- **SPEC1**: All stored identifying images and dashcam footage must be encrypted at rest using AES-256 (or equivalent) with per-object keys managed by a centralized KMS/HSM; the software must enforce that decryption keys are only available to processes/roles explicitly authorized by IAM policies and must rotate keys at least every 90 days.
- **SPEC2**: All network transfers of identifying images or location metadata must use mutually authenticated TLS (minimum TLS 1.2) with strict certificate validation; client applications must validate server certificates and support certificate pinning or equivalent to prevent man-in-the-middle tampering.
- **SPEC3**: Access to any identifying images, footage, or precise location information must require authenticated accounts with role-based authorization and active MFA; the software must issue time-limited, scoped access tokens (maximum lifetime 15 minutes) and record an immutable audit log entry for each access attempt (user ID, role, timestamp, object ID, action, source IP) retained for at least 1 year and available for review.
- **SPEC4**: Before a recipient is authenticated and authorized, the software must not expose high-resolution images or precise GPS coordinates. For any unauthenticated or public-facing view the software provides only downsampled, obfuscated thumbnails (maximum 200x200 pixels with an applied blur of at least Gaussian sigma=2) and location coarsened to no finer than a 1 km radius. The software must record explicit parental/guardian consent and log that consent before allowing any download or external sharing of original-resolution images or exact location data.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Images or location information are reused or distributed beyond the coordinated search, enabling stalking, extortion, or other targeted harms against the child or family.

**Requirement (REQ4):** Identifying images, live location, and location-linked data are not disclosed to third parties outside the coordinated search team (authorized investigators and designated non-profit personnel) for purposes that enable stalking, harassment, or public dissemination.

**Assumptions (ASM):**

- **ASM1**: An authoritative, regularly updated roster of coordinated search team members and their roles is maintained by the sponsoring agency or non-profit and is available to the system in a verifiable format (e.g., signed list, federation feed) so the system can determine which accounts are authorized for a given case.
- **ASM2**: Authorized investigators and designated non-profit personnel use devices and accounts that support the authentication methods required by the system (e.g., multi-factor authentication), and those devices can receive authentication challenges or confirmations when required.
- **ASM3**: Organizational and legal policies governing the coordinated search prohibit external sharing of identifying images, live location, or location-linked data outside the authorized team, and there exist mechanisms (investigations, sanctions) outside the software environment to respond to violations.

**Specifications (SPEC):**

- **SPEC1**: Enforce case- and role-based access control: the software must allow access to identifying images, live location, and location-linked data only to authenticated accounts that are listed as authorized for that specific case and role; every access must be checked against the current authoritative roster before returning data.
- **SPEC2**: Purpose-limited access and export control: every request to view, export, or transmit identifying images or precise location data must include a declared purpose and be checked against allowed purposes for the user’s role and case; the software must block or require escalation for any access or export attempt whose purpose is not permitted.
- **SPEC3**: Least-privilege presentation and download restrictions: the software must present only redacted/low-resolution images and coarse location (e.g., blurred image, rounded coordinates or bounding radius) to users without explicit case-level authorization, and must prevent downloading or screen-capture of full-resolution images and exact coordinates unless the user has explicit, logged authorization and has completed required MFA confirmation.
- **SPEC4**: Auditing, tamper-evident logs, and external-sharing alerts: the software must record immutable audit log entries for every view, export, transmission, or sharing action involving identifying images or live location (including user ID, role, timestamp, purpose, data identifiers, and destination); logs must be tamper-evident and retained per policy, and the system must generate automatic alerts for any attempted or completed exports to external destinations (non-rostered accounts, public URLs, or social platforms).

#### H5 / REQ5

**Related Goal:** G5

**Loss:** Search activities impose unexpected mobile-data charges, drain device battery, or consume storage on the parent's devices, creating financial burden or preventing the parent from communicating or participating in the search.

**Requirement (REQ5):** Search operations that involve a parent's devices do not cause unanticipated monetary charges, excessive battery depletion, or storage exhaustion on those devices that would prevent the parent from participating in search activities or essential communications.

**Assumptions (ASM):**

- **ASM1**: Mobile network carriers bill data transferred over cellular networks on a metered basis (per-byte, caps, or overage charges) and those charges are tied to the parent device's cellular usage.
- **ASM2**: The parent's device operating system exposes accurate, real‑time indicators via APIs for current network type (cellular vs. Wi‑Fi), battery level (percentage), charging state, and available storage (bytes free), and those indicators reflect actual device state.
- **ASM3**: The parent (or legal guardian) can and will configure or respond to in‑app permission and preference prompts (e.g., to allow cellular uploads, background operation, or additional storage use) within a timeframe that is useful for search operations, or will explicitly deny them.

**Specifications (SPEC):**

- **SPEC1**: The software must detect current network type via OS APIs and enforce a default policy that defers any upload of media files larger than 500 KB when the device is on a cellular connection unless the parent has explicitly granted per‑case or global consent for cellular uploads; the software must present a clear consent prompt before any deferred upload proceeds and record the parent's response (timestamp, case id, bytes consented) in an audit log.
- **SPEC2**: The software must continuously monitor battery level and charging state and suspend non‑critical background search activities (including periodic camera scans, high‑frequency GPS polling, and non‑urgent uploads) when battery level falls below 20% and the device is not charging; when suspension occurs the software must notify the parent and provide an immediate override option that requires explicit confirmation and logs the override.
- **SPEC3**: Before downloading, caching, or saving any media to the parent's device, the software must check available storage and enforce that any operation will leave at least 50 MB free and will not exceed a per‑case cache quota (default 200 MB); if the operation would violate either condition, the software must refuse the operation, notify the parent with remediation options (e.g., free space, change quota, defer), and log the refusal with the available free space measurement.
- **SPEC4**: The software must perform on‑device ML inference to filter candidate sightings and attach a numeric confidence score to each candidate; by default the software must only transmit low‑bandwidth metadata and compressed thumbnails over cellular, and transmit full‑resolution media only when (a) confidence >= configurable threshold (default 0.7) and (b) network is Wi‑Fi or device is charging, or when the parent explicitly approves a cellular full‑media upload; every transmission must record transmitted byte counts, ML confidence, and the consent/no‑consent state for auditing.

## 3. Dashcam owner / vehicle owner

### Goals

- **G1**: Maintain control over who can access or receive dashcam footage and associated location information.
- **G2**: Avoid unexpected financial costs and excessive use of device resources (mobile data, battery, storage) from search activities.
- **G3**: Avoid being implicated, harassed, or legally exposed due to false or incorrect person-recognition results.
- **G4**: Ensure dashcam operation does not compromise vehicle operability or driver safety.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Identifying images or precise location data from the dashcam are accessed or shared with third parties without the owner's consent, causing privacy invasion, stalking, or reputational harm.

**Requirement (REQ1):** Identifying images and precise location information from the dashcam are not accessible to or shared with third parties except when the owner has explicitly permitted that specific access or sharing.

**Assumptions (ASM):**

- **ASM1**: The dashcam hardware provides GPS coordinates and timestamps as sensor outputs that the software can read from the device (i.e., location and time metadata are available to the software when a frame is recorded).
- **ASM2**: When the owner grants or denies permission for sharing a specific image or precise location, the owner performs an authenticated action (e.g., via the device UI or owner mobile app) that produces an observable, verifiable consent record or token that the software can retrieve and validate.
- **ASM3**: Network and cloud infrastructure in the environment permit outbound transmission to third-party endpoints only when an active network connection is available; attempted transmissions will either succeed or fail and these outcomes are observable by the software (i.e., the software can detect whether data was actually transmitted).

**Specifications (SPEC):**

- **SPEC1**: Store all identifying images and any precise location metadata encrypted at rest using keys tied to owner-controlled credentials or a device secure element; the software must refuse to return decrypted image pixels or precise coordinates to any requesting principal that has not been authenticated and authorized as the owner or an owner-designated account.
- **SPEC2**: Before any export, transmission, or sharing of an image or precise location to an external recipient, require a verifiable consent record: validate a received consent token (matching ASM2) and record a signed audit entry including the image identifier, precise location identifier, recipient identifier, consent token ID, and timestamp; if no valid consent token exists, block the sharing operation and log the blocked attempt.
- **SPEC3**: Enforce access control for APIs and UIs that expose images or precise location: authenticate users via the configured identity provider, authorize access only if the authenticated identity equals the owner or an owner-authorized account, and require a second factor for any remote retrieval of identifying images or precise coordinates; log successful and failed access attempts with principal ID and reason.
- **SPEC4**: When ML-based detection runs on images, the software must not automatically upload original images or precise GPS coordinates to any external endpoint without validated owner consent; for remote matching or reporting allow only non-identifying artifacts (e.g., feature hashes, blurred images, or coarse-grained location above a configurable radius) to be transmitted unless a valid consent token permitting transmission of full-resolution image and precise coordinates is present.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Unexpected mobile data charges, depleted storage, or excessive battery use occur because of search-related uploads or prolonged processing, causing financial loss or loss of recording capability.

**Requirement (REQ2):** Any data transfers or operations that would consume the owner's metered cellular data, substantially exceed the owner's available storage, or significantly drain the device battery occur only with the owner's explicit consent or within the owner's configured data, storage, and power limits.

**Assumptions (ASM):**

- **ASM1**: The device operating system or modem exposes runtime indicators that reliably report current network connectivity type (e.g., cellular vs. Wi‑Fi) and whether the current connection is metered/costed.
- **ASM2**: The device hardware and OS provide accurate, queryable measurements of available persistent storage, current battery charge level (percentage) and charging status, and these measurements reflect the actual resources the device can use.
- **ASM3**: The owner can configure consent preferences and quantitative limits (cellular data allowance, minimum reserved free storage, minimum battery level for heavy processing) via the device UI prior to or during operation, and those preferences are persisted and accessible to the software at runtime.

**Specifications (SPEC):**

- **SPEC1**: Before initiating any network transfer that the OS reports as metered (cellular), the software shall check the owner's stored preference and remaining user-configured cellular allowance; if the preference disallows cellular uploads or the estimated upload size exceeds the remaining allowance, the software shall not start the transfer, shall queue the payload for transfer on unmetered networks, and shall present or log a user-facing consent prompt that includes an estimated data size and the allowance remaining when owner interaction is required.
- **SPEC2**: Prior to starting any on‑device processing or upload that requires temporary or permanent storage, the software shall compute the estimated storage required (including temporary working space) and compare against available storage minus the owner's configured minimum free-storage reservation; if available storage would fall below the configured reservation, the software shall not start the operation and shall notify the owner with options to (a) cancel, (b) delete selectable old recordings per the owner's retention policy, or (c) explicitly override for this operation; all owner overrides must be logged with timestamp and operation identifier.
- **SPEC3**: Before performing energy‑intensive processing or uploads, the software shall check the device battery percentage and charging status and compare against the owner's configured battery threshold; if battery is below the threshold and the device is not charging, the software shall defer the operation, provide a consent prompt showing expected duration and battery impact, and only proceed if the owner explicitly permits continuation; the software shall also offer a lower‑power fallback mode (e.g., coarser analysis or reduced upload size) and honor the owner's choice.
- **SPEC4**: When an ML model triggers a candidate sighting, the software shall retain detection results locally and shall not automatically upload the associated media over a metered connection unless the owner's consent or configured policy allows it; for each candidate the software shall estimate upload size, increment a persisted per‑day cellular‑usage counter before attempting uploads, and block or defer further cellular uploads when the owner's configured daily cellular cap is reached, retrying queued uploads only when an unmetered connection is detected or after renewed owner consent.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Automated person-recognition produces false matches that lead authorities or others to treat innocent people recorded by the owner's dashcam as confirmed sightings, resulting in investigations, confrontations, or legal exposure for the owner.

**Requirement (REQ3):** People who are not the missing child are not reported to investigators or treated as confirmed sightings solely on the basis of automated person-recognition outputs.

**Assumptions (ASM):**

- **ASM1**: Authorized human verifiers (investigators or trained personnel) will review candidate sightings before taking enforcement action or publicly disseminating information about a sighting.
- **ASM2**: Dashcam capture metadata (GPS and timestamp) accurately reflect the real-world capture: GPS coordinates are within 50 meters of the actual capture location and timestamps are synchronized to real-world time within 5 seconds.
- **ASM3**: Reference images supplied for a missing-child case depict the correct child and include at least one unobstructed frontal-face image with resolution >= 640x480.

**Specifications (SPEC):**

- **SPEC1**: Label and store every automated person-recognition result as a 'candidate_sighting' (never as 'confirmed') and include alongside it: model confidence score, detected bounding box, capture timestamp, GPS coordinates, reference-image ID, and ML model version.
- **SPEC2**: Do not send automatic notifications to law enforcement or publish sightings externally based solely on automated outputs; candidate_sightings may be prioritized by confidence but must remain internal until explicitly escalated by a human verifier.
- **SPEC3**: Require at least one authorized human verifier to view the raw image/video and a visual comparison overlay and then perform an explicit action that records verifier identity, confirmation timestamp, and a textual justification before the software permits changing a candidate_sighting status to 'confirmed' or forwarding it externally.
- **SPEC4**: Produce and protect a tamper-evident audit log for every candidate_sighting that records raw ML outputs, confidence scores, model version, reference image ID, all access events, and all status changes; support exporting the log for legal or investigative review.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Dashcam search operations deplete the vehicle battery or consume critical device resources so the vehicle cannot start or essential driving functions are impaired, creating safety risks or significant inconvenience for the owner.

**Requirement (REQ4):** Search operations do not cause vehicle battery level or availability of critical vehicle systems to fall below the levels required for normal vehicle start-up and safe operation given the owner's configured power and performance preferences.

**Assumptions (ASM):**

- **ASM1**: The vehicle exposes battery state and related electrical telemetry (state-of-charge or voltage, charging status, and battery health indicators) via a documented API or CAN-bus interface and those telemetry values reflect the real battery state within a verifiable tolerance (e.g., ±5% SOC) and update at least once per minute.
- **ASM2**: When the engine is running the vehicle alternator/charging system provides a measurable net charging current (or lack thereof when not running) that can be observed via the vehicle telemetry; when the engine is off the baseline parasitic/background drain rate is approximately stable and can be estimated from past observations.
- **ASM3**: The owner’s power and performance preferences (including minimum acceptable battery level for start/operation and permitted aggressive search modes) are persisted in vehicle/user settings and remain available to the software at run time as authoritative configuration.
- **ASM4**: A concrete minimum battery requirement for normal vehicle start-up and critical-system operation (expressed as SOC, voltage, or other metric) exists and is obtainable from vehicle metadata or manufacturer specifications so the software can compare measured/predicted battery state against that requirement.

**Specifications (SPEC):**

- **SPEC1**: Continuously monitor battery telemetry and charging status at least once per minute; compute a projected battery state over the next configurable planning horizon (default 30 minutes) that accounts for current background drain, measured/predicted energy cost of ongoing search operations, and observed charging when the engine is running; suspend or throttle any search activity if the projection shows battery state falling below the owner-configured minimum plus a configurable safety margin.
- **SPEC2**: Measure and maintain running estimates of energy cost for each search-related action (camera capture, ML inference at each fidelity level, network transmission, and storage I/O) using recent empirical measurements; use a conservative bound (e.g., 95th percentile) of these estimates when predicting battery impact and update these estimates at least daily or after any firmware/model update.
- **SPEC3**: Provide a hierarchical mitigation policy: (a) reduce ML/model fidelity or sampling frequency to lower-power modes when projections approach the owner threshold, (b) if reduction is insufficient, pause nonessential search tasks and reduce sensor/network use, and (c) if battery still projects below threshold, persist state of paused tasks and stop all search operations; record the reason/timestamp/battery state and notify the owner via local vehicle UI (and remote notification where connectivity exists).
- **SPEC4**: Log all battery readings, projections, energy-cost estimates, mitigation actions (throttle/pause/resume), and owner preference values to persistent storage for retestability; include a test-mode that can simulate specified battery states, charging conditions, and search loads so that compliance with the owner-configured thresholds and mitigation behaviors can be validated in controlled tests.

## 4. Vehicle occupants and passengers

### Goals

- **G1**: Control over personal images and location data collected by the dashcam
- **G2**: Not being wrongfully identified or subjected to law-enforcement or investigatory action because of automated matches
- **G3**: Avoiding unexpected monetary or resource burdens (mobile data, battery, storage) caused by search operations
- **G4**: Protection from unauthorized access, secondary use, or misuse of recorded footage and derived results

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Vehicle occupants are recorded, and their images or location history are retained or disclosed without their consent, enabling unwanted surveillance or exposure of private activities.

**Requirement (REQ1):** Images and location information of vehicle occupants are not disclosed to investigators, third parties, or other external parties without the occupants' consent or a verified lawful request.

**Assumptions (ASM):**

- **ASM1**: The vehicle's cameras, GPS, and system clock produce metadata (timestamps and location) that are consistently available to the software and are synchronized to an authoritative time source often enough to correlate images with location and consent events.
- **ASM2**: Occupants can provide and revoke consent through a physical or authenticated in-vehicle input mechanism (e.g., touchscreen confirmation, seat-specific token, or user account login) whose events are observable and logged by the software at the time of input.
- **ASM3**: Authorized external requesters (e.g., law enforcement) present verifiable digital legal requests that are signed by a recognized authority and can be validated against an available verification service or trust anchor reachable by the vehicle or backend within a bounded operational period.

**Specifications (SPEC):**

- **SPEC1**: All images and occupant location history must be encrypted at rest and in transit using keys managed by the system. The software must permit decryption of such data only when (a) a valid consent record exists for the requested data scope, or (b) a digital legal request has been cryptographically verified by the software. Any attempt to export decrypted occupant-identifying data without one of these conditions must be denied and logged.
- **SPEC2**: The software must maintain a consent ledger recording: occupant session identifier, scope of consent (images, location, duration), timestamp of consent/grant, and revocation timestamp. Before any disclosure action, the software must check the ledger and allow disclosure only if the consent record explicitly covers the requested data and is not revoked; revocation must immediately prevent subsequent disclosures and be enforced by the access control check.
- **SPEC3**: Upon receiving a request to disclose occupant images or location history, the software must validate the request by verifying a digital signature against configured trust anchors, confirm the request's scope and validity period, and record the verification result and all relevant request metadata in an immutable audit log. If signature verification or scope/validity checks fail, the software must deny disclosure.
- **SPEC4**: The software must minimize shared data for any permitted disclosure: it must (a) attach only fields required by the consent or verified request, (b) automatically redact or blur faces of occupants not matched by the request's scope, and (c) require a human reviewer to confirm any ML-identified occupant match before releasing identifying imagery or precise location traces. All redaction or reviewer decisions must be recorded in the audit log.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Occupants are falsely identified as the missing child and subjected to interrogation, detention, reputational damage, or emotional distress due to an automated match.

**Requirement (REQ2):** People who are not the missing child are not treated as confirmed sightings or subjected to investigatory action solely on the basis of automated person-recognition outputs.

**Assumptions (ASM):**

- **ASM1**: Human investigators or authorized human reviewers will receive candidate sighting reports and will review each received candidate sighting within 24 hours of receipt.
- **ASM2**: Vehicle occupants (or a reachable vehicle owner/driver) can be contacted by investigators at the time of review and can, if present, provide corroborating identity information (e.g., government-issued ID or caregiver contact) to confirm identity.
- **ASM3**: The dashcam hardware and device environment supply observable metadata with sufficient fidelity for human verification: captured face images meet a minimum legibility threshold (e.g., face region >= specified pixel area), device clock is synchronized to network time within ±5 seconds, and GNSS location accuracy is within 10 meters.

**Specifications (SPEC):**

- **SPEC1**: The software must label all automated person-recognition outputs and related camera captures as 'candidate sighting' (never 'confirmed') in all UIs and exported reports, display the ML match confidence score and ML model version alongside each candidate, and show a persistent, human-readable disclaimer that automated outputs are probabilistic and not sufficient for detention or other investigatory action.
- **SPEC2**: The software must not generate or transmit any automatic report, alert, or action that requests or instructs detention, interrogation, or other enforcement action based solely on an automated person-recognition output; any escalation to external agencies or enforcement workflows must be gated by an explicit, logged human reviewer confirmation action in the system UI.
- **SPEC3**: For every candidate sighting the software must record and persist an auditable package including: captured media (images/video), capture timestamp, device-reported GPS coordinates, match confidence score, ML model identifier and version, the identity of any human reviewer who accessed the item, reviewer decisions and timestamps, and any outbound messages; these audit records must be exportable and retained for at least 2 years.
- **SPEC4**: The software must restrict access to candidate sightings and their supporting data to authenticated, authorized roles; require reviewers to acknowledge a 'no-automated-detention' policy before viewing sensitive media; and require completion of a mandatory checklist (e.g., attempt contact, request ID/caregiver info, verify location) in the UI before enabling any 'confirm sighting' action.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Search activities consume occupants' mobile data, battery, or storage unexpectedly, causing monetary charges, loss of critical device function, or reduced safety during travel.

**Requirement (REQ3):** Search operations do not consume occupants' mobile data allowance, significant battery capacity, or device storage without prior, informed consent from the affected occupants.

**Assumptions (ASM):**

- **ASM1**: The device operating system exposes accurate, queryable, app-specific metrics for mobile data bytes sent/received, battery state (percentage and charging status), and available persistent storage (free bytes) through documented APIs accessible to the dashcam software at runtime.
- **ASM2**: At least one vehicle occupant is present with an unlocked, responsive interface (vehicle touchscreen or paired mobile device) that can display a consent dialog and record a clear affirmative/negative response before a resource-consuming search operation begins.
- **ASM3**: The vehicle will encounter a non-cellular transfer opportunity (e.g., known Wi‑Fi, wired upload point, or vehicle-mounted network) or a charging event often enough that uploads or deferred processing postponed from cellular or low-battery periods can reasonably complete within an operationally defined maximum delay (for example, within 24 hours).

**Specifications (SPEC):**

- **SPEC1**: Before initiating any network transfer that would use cellular data, the software must query app-specific cellular data usage and the occupant's consent setting; if explicit consent for cellular uploads of search-related data is not recorded, the software must queue data locally and defer all cellular uploads until a non-cellular network is available or explicit consent is obtained.
- **SPEC2**: The software must monitor device battery percentage and charging state and must not begin or continue prolonged search activities (including continuous ML inference or data uploads estimated to consume more than a configurable battery budget) when battery is below a configurable threshold (default 20%) unless an explicit, informed consent is recorded for that specific activity and the consent is logged with timestamp and account identifier.
- **SPEC3**: The software must enforce a configurable storage quota for cached search artifacts (images, clips, feature data). If accepting new artifacts would exceed the quota or reduce available device storage below a configurable minimum, the software must pause saving new artifacts and present occupants with a clear choice to (a) increase the quota (requiring explicit consent), (b) purge older artifacts, or (c) cancel the new save; the chosen option and consent (if any) must be recorded.
- **SPEC4**: By default perform ML inference on-device; the software must not transmit raw images, extracted feature vectors, or model outputs to remote servers over cellular networks without explicit prior consent. If cloud processing is requested and consent is given, the software must (a) estimate and display the expected data volume for the requested upload, (b) obtain per-upload or per-session consent, and (c) log the consent and actual bytes transmitted.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Unauthorized parties—including contractors, attackers, or other third parties—gain access to identifying footage or search results and use them for stalking, blackmail, discrimination, or other harms.

**Requirement (REQ4):** Unauthorized parties do not gain access to identifying images or location information from dashcam recordings or from search results.

**Assumptions (ASM):**

- **ASM1**: Physical custody of the dashcam device and any removable storage is controlled by vehicle occupants or authorized custodians; lost or stolen devices are reported to the system operator within 24 hours.
- **ASM2**: User account credentials and multi-factor authentication (MFA) tokens for accounts that can access dashcam footage or search results are kept confidential by their owners and are not intentionally shared with third parties.
- **ASM3**: Requests from investigators, contractors, or third parties for full identifying footage or precise location are accompanied by externally issued, verifiable authorization artifacts (e.g., signed organizational authorization, legal warrant, or approved request token) produced by authorized human/legal processes.

**Specifications (SPEC):**

- **SPEC1**: Encrypt all identifying images and associated location metadata at rest using AES-256 (or equivalent) with keys stored in a hardware-backed key store; require server-side authorization and key-material retrieval before decrypting or returning any unredacted data.
- **SPEC2**: Enforce role-based access control server-side: require authenticated sessions with MFA for any account that requests identifying images or precise location; verify role permissions and a valid authorization artifact before returning unredacted images or exact coordinates; deny and log requests failing authorization.
- **SPEC3**: Present search results by default in redacted/anonymized form: automatically blur faces and unique identifiers in images and coarse-grain location to a configurable radius (e.g., >=1 km); include ML candidate confidence scores and metadata but do not reveal identity or precise coordinates until an authorized, audited approval is recorded.
- **SPEC4**: Produce immutable, tamper-evident audit logs for every access to identifying images or precise location (including requester ID, authorization artifact ID, timestamp, resource ID, and action); store logs off-device, provide automated alerts for anomalous access patterns, and support immediate revocation of access tokens and remote key/data wipe.

## 5. Law enforcement agencies / police investigators

### Goals

- **G1**: Obtain timely, actionable leads so investigators can follow up during critical early search windows.
- **G2**: Minimize false leads and avoid misidentification of innocent people to preserve investigative resources and protect civilians.
- **G3**: Preserve evidentiary integrity and provable provenance so information can be validated and used in legal processes.
- **G4**: Protect sensitive imagery and location data to prevent unauthorized disclosure that could endanger individuals or compromise investigations.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Investigators receive sightings too late to act effectively, causing missed opportunities to locate the missing child.

**Requirement (REQ1):** Investigators receive relevant sightings within a timeframe appropriate for active missing-child searches (i.e., hours rather than days) so that follow-up actions can be initiated while search windows remain viable.

**Assumptions (ASM):**

- **ASM1**: During the active search window, at least one operational dashcam‑equipped vehicle enters the investigator‑defined geographic search area such that, if the child is present in public view in that area, a dashcam could capture images or video of the child.
- **ASM2**: Dashcam devices provide accurate capture metadata: device clock and timestamps are synchronized to reference time within ±5 seconds and GPS/location fixes are accurate within ±10 meters at the time of capture.
- **ASM3**: Captured media contain sufficient visual information for automated detection (e.g., resolution >= 720p and the child’s face or body occupies a sufficiently unobstructed portion of the frame to allow detection), or else the capture will be recognizable by a human reviewer.

**Specifications (SPEC):**

- **SPEC1**: For every candidate sighting detected on‑device or at the server, the software must create a candidate sighting record that includes: capture timestamp, GPS/location, device ID, media hash, media excerpt or frame, ML detection bounding box(es), model version, and model confidence score; the record must be labeled explicitly as a 'candidate sighting' (not confirmed).
- **SPEC2**: The software must implement a transmission and retry policy: queue candidate sighting records for upload immediately, persist them locally until acknowledged by the server, perform exponential backoff retries on failure, and log all transmission attempts and delays. The system must expose metrics showing time from capture timestamp to successful server receipt for each sighting.
- **SPEC3**: The central system must prioritize and notify investigators of recent candidate sightings by applying configurable rules that include recency (e.g., capture within the last X hours) and model confidence thresholds; for prioritized items the system must automatically deliver an investigator alert containing media preview, location, timestamp, confidence score, and model version.
- **SPEC4**: The software must provide immutable provenance and audit records for each candidate sighting (media hash, original media or frame pointer, capture metadata, ML outputs, device ID, transmission timestamps and statuses) and an API allowing investigators to query and filter sightings by time window, location, and confidence; the API must also return the model operating point and historically measured false positive/false negative rates associated with the model version used to generate the candidate.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** High rates of false positives lead to wasted investigator time, diversion of resources, and potential reputational or emotional harm to innocent people contacted as suspected sightings.

**Requirement (REQ2):** People who do not match the missing child are not reported to investigators as confirmed sightings solely because of an automated prediction; reported items to investigators are presented as leads that require independent validation.

**Assumptions (ASM):**

- **ASM1**: Authorized investigators will retrieve and review candidate sightings delivered by the system within 48 hours of notification.
- **ASM2**: Dashcam devices and ingest infrastructure provide accurate embedded timestamps and GPS coordinates in recorded media, with device clock drift no greater than 10 seconds relative to network time.
- **ASM3**: Investigators have lawful access to, and operational ability to obtain, original full-resolution video frames, associated metadata, and any local witness/contact information needed to independently validate a candidate sighting.

**Specifications (SPEC):**

- **SPEC1**: The software shall label every automated detection delivered to investigators as a 'candidate sighting' (or equivalent) and shall never mark or display such items as 'confirmed sighting' or equivalent without an explicit investigator confirmation action.
- **SPEC2**: For each candidate sighting the software shall present provenance and uncertainty: include the original video file or extracted frame(s), bounding box overlays, device timestamp, GPS coordinates, model confidence score, and model version; the system shall use a default conservative notification threshold of 0.85 confidence (configurable by an authorized administrator), suppressing outward investigator notifications for detections below that threshold while still recording them in an internal review queue.
- **SPEC3**: The software shall require an explicit human-in-the-loop confirmation before changing a candidate sighting's status to 'confirmed': the action must record the confirmer's user ID, timestamp, the evidence reviewed (selected frames/segments), and a short justification; no automated rule or ML output alone may change status to 'confirmed'.
- **SPEC4**: The software shall prevent automatic dissemination of candidate sightings to third parties or public channels: notifications to investigators must be rate-limited to at most 5 notifications per missing-child case per 24-hour period, automatically group likely-duplicate detections (e.g., within 500 meters and 30 minutes) into a single lead, and record an auditable log of all notifications, grouping decisions, and access to underlying media.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Reported footage or metadata lack verifiable provenance, causing evidence to be inadmissible or unusable for formal investigation and legal proceedings.

**Requirement (REQ3):** Each sighting reported to investigators is accompanied by verifiable contextual information (such as original capture time, location reference, and a traceable record of handling) sufficient for investigators to validate provenance and document chain-of-possession for investigative and legal use.

**Assumptions (ASM):**

- **ASM1**: Dashcam devices that capture candidate sightings have access to a reliable, tamper-resistant time source (e.g., GPS time or a hardware real-time clock with write-protection) and record capture times with a documented uncertainty relative to UTC.
- **ASM2**: Dashcam devices that capture candidate sightings can obtain a geolocation fix (e.g., GPS) at the time of capture and expose that geolocation and its reported accuracy to the device software for inclusion in metadata.
- **ASM3**: A trusted authority/PKI and corresponding trust anchors accessible to investigators exist in the operational environment and can be used to map device identifiers to authoritative identities and to verify cryptographic signatures produced by devices.

**Specifications (SPEC):**

- **SPEC1**: On initial capture, the software must record and persist the original_capture_time and original_location metadata fields (including stated accuracy/uncertainty), compute and store a content integrity hash (e.g., SHA-256) of the raw footage file and of the metadata blob, and (where a device-held private key is available) attach a device signature over the hash and metadata. The software must never overwrite original_capture_time or original_location fields with upload/processing timestamps.
- **SPEC2**: The system must maintain an append-only, tamper-evident audit log of all handling events for each sighting (events: capture, local modification, upload, receipt, access by user, export, deletion). Each audit entry must include actor identity (user or system component), role, action, and timestamp; entries must be cryptographically chained (e.g., hash chain) and signed by the server or gateway key. The system shall provide an exportable chain-of-custody report containing the full audit log and signatures for investigator use.
- **SPEC3**: When an ML model flags footage as a candidate sighting, the software must attach machine-provenance metadata: model identifier and version, model container/hash, inference timestamp, input frame hashes, detection confidence score, and an explicit label that the sighting is a 'model-generated candidate' (not a confirmed sighting). This metadata must be included in the same integrity/signed package referenced in SPEC1.
- **SPEC4**: Before sending or presenting a sighting package to investigators, the software must attempt to verify any device-provided signature and certificate chain against locally configured trust anchors. The delivered package must include: original footage, original metadata (time/location/accuracy), content hashes, device signature and certificate chain, verification result (success/failure) with reason if failure, and the full audit log. If verification cannot be completed, the package must be marked 'unverifiable' and include detailed diagnostic evidence for investigators.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Unauthorized access to identifying images or location information exposes the child or other parties to privacy violations, harassment, or interference with the investigation.

**Requirement (REQ4):** Unauthorized parties do not gain access to identifying images, footage, or location information related to missing-child searches.

**Assumptions (ASM):**

- **ASM1**: Network connectivity between dashcams, cloud servers, and investigator consoles allows the software to establish and maintain encrypted channels (e.g., TLS) so the system can detect and use secure transport for data in transit.
- **ASM2**: Authorized investigator accounts and role memberships are provisioned and maintained in the system's identity provider, and the identity provider exposes accurate account and role information via authenticated queries the software can perform.
- **ASM3**: Physical custody and device-management processes prevent unauthorized physical access or compromise of dashcam and investigator endpoint private keys; if an endpoint is revoked or compromised, the environment will make revocation information available to the system in a timely manner.

**Specifications (SPEC):**

- **SPEC1**: Require per-request authentication and authorization checks: only accounts with an authorized role (e.g., investigator) and an explicit permission flag may access identifying images, footage, or precise location metadata; access to such assets must require multi-factor authentication for the requesting account.
- **SPEC2**: Encrypt identifying images, footage, and location data at rest using strong cryptography (e.g., AES-256) with keys stored and managed in a dedicated KMS separate from the storage system; transmit all such data over authenticated encrypted channels (TLS 1.2+ with server and client authentication).
- **SPEC3**: Record a tamper-evident audit trail for every access to identifying assets capturing: user ID, role, timestamp, asset ID, action type (view/download/share), client IP/device ID, and stated justification; store logs in append-only storage and provide queryable reports and real-time alerts for anomalous access patterns (e.g., bulk exports or access outside normal hours).
- **SPEC4**: Default presentation and API behavior must minimize exposure: return only redacted or low-resolution thumbnails with obfuscated faces and masked location data. Require an explicit human review and an 'authorize_release' action by an authorized investigator before returning full-resolution images or precise GPS coordinates to any user or external party. Label ML-generated candidate detections as 'candidate' and prevent automated release of identifying data without human confirmation.

## 6. Non-profit child-safety organization

### Goals

- **G1**: Coordinate effective, timely searches that produce actionable leads for investigators and families.
- **G2**: Protect the privacy and safety of children and families involved in searches.
- **G3**: Maintain public trust and ensure ethical use of the system and data.
- **G4**: Ensure equitable and reliable detection across demographic groups and deployment contexts.
- **G5**: Avoid overloading organizational resources or investigators with low-value or duplicate alerts.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Investigators and families are diverted by false-positive matches (innocent people reported as sightings), causing wasted search resources, unnecessary distress to families, and potential legal or reputational exposure for the organization.

**Requirement (REQ1):** Sightings communicated to investigators or families are supported by corroboration beyond an unverified automated match; investigators and operational partners do not act on or publicize uncorroborated automated-only matches as confirmed sightings.

**Assumptions (ASM):**

- **ASM1**: Designated investigators and operational partners are reachable via contact methods registered in the system and will review received candidate sightings within 24 hours of receipt.
- **ASM2**: Camera devices and third-party media sources that capture candidate sightings embed or provide machine-readable time and location metadata (timestamps and GPS) with a clock skew of no more than ±5 seconds and location accuracy within 20 meters, and the software can extract those fields from submitted media.
- **ASM3**: Bystanders or eyewitnesses who can provide corroborating media or statements are contactable and, when available, can supply media or structured corroboration (e.g., a photo or short video with device metadata or a signed statement) within 48 hours of being asked.

**Specifications (SPEC):**

- **SPEC1**: Label every ML-produced detection as a 'candidate sighting' in all system views and outputs; include with each candidate an evidence bundle containing the raw media clip (or reference), extracted timestamp and geolocation metadata, source device identifier, ML model identifier and version, ML confidence score, similarity metric(s), and detection bounding box or mask. The software must never change candidate sightings to a 'confirmed' public status automatically based solely on ML outputs.
- **SPEC2**: Before any investigator-level 'confirmed' status, family notification, or public dissemination is permitted, require at least one of the following corroboration conditions be satisfied and explicitly recorded: (A) an authorized human reviewer executes a verification action in the system UI (the action and reviewer identity are logged), OR (B) an independent corroborating source is attached (media from a different device identifier than the original source with timestamp within ±10 seconds and geolocation within 50 meters of the primary detection). The software must enforce these rules and prevent status transitions to 'confirmed' unless one of these recorded conditions is present.
- **SPEC3**: Deliver candidate-only alerts to investigators with the full evidence bundle and a clear label 'candidate — unverified'. Do not send automated notifications to families or public channels for candidate-only matches. The UI/API must block any attempt to send family-facing or public-facing notifications for recordings that are not in 'confirmed' state; attempts by users to override this block must require a secondary authorization step and must be recorded in the audit log.
- **SPEC4**: Maintain an auditable trail for every candidate and confirmed sighting that records timestamps of detection receipt, ML model id/version, ML confidence, all attached evidence items, all verification actions (user id, role, time, and decision), and any notifications sent. Retain raw media and the audit trail for at least 90 days and provide exportable evidence bundles for investigators. The system must provide queryable status (candidate vs confirmed) and a report of which corroboration condition satisfied confirmation.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Identifying images or precise location information about children or families are exposed to unauthorized parties (public, press, or malicious actors), causing privacy violations, safety risks for children, and loss of trust in the organization.

**Requirement (REQ2):** Identifying images, precise location data, and case-specific sensitive information are disclosed only to authorized investigators and designated organizational partners involved in the active case; unauthorized disclosure to the public or unrelated third parties does not occur.

**Assumptions (ASM):**

- **ASM1**: The organization's identity provider (IdP) contains up-to-date account, role, and membership information for investigators and partner organizations and is queryable by the software at request time.
- **ASM2**: Network and communications channels used to deliver sensitive data to investigators and partners support authenticated, encrypted transport (e.g., TLS) so that the software can transmit data over secure channels to authorized endpoints.
- **ASM3**: Case metadata (case status such as active/inactive, assigned investigators/partners, and any legal/consent restrictions) is recorded as authoritative structured data in the organization's case management system and is available to the software via an API.

**Specifications (SPEC):**

- **SPEC1**: Require per-request authentication and authorization: every request to view identifying images, precise location, or case-specific sensitive data must be authenticated (MFA-enabled) and authorized by verifying the user's account status, role, and explicit assignment to the specific active case via the IdP and case-management API; deny access if any check fails.
- **SPEC2**: Encrypt sensitive data at rest and in transit with per-case cryptographic keys: store identifying images, precise GPS/location metadata, and case-sensitive fields encrypted at rest using keys scoped to the case; decryption requires a valid case-access token verified against current case membership; enforce key rotation and log all key-access events.
- **SPEC3**: Control automated ML outputs and require human authorization for full disclosure: automated notifications or public endpoints must not include full-resolution identifying images or precise coordinates; only provide redacted thumbnails (e.g., blurred faces), coarse location (e.g., city/zip), and model confidence. Full-resolution images and precise locations may be released only after an explicit, recorded approval action by an authorized investigator assigned to the case, and only via an authenticated UI or approved secure transmission.
- **SPEC4**: Audit, monitoring, and alerting: record immutable audit logs for every access, attempted access, decryption, export, or external share of sensitive data including user id, role, timestamp, case id, data elements accessed, and destination; retain logs for at least 7 years; automatically generate alerts to the security team within one hour for anomalous events (e.g., access by a user not assigned to the case, large-volume exports, or repeated failed authorization attempts).

#### H3 / REQ3

**Related Goal:** G4

**Loss:** The system consistently misses or under-reports appearances of missing children from certain demographic groups or geographic areas, leading to unequal service, reduced recovery chances for those children, and reputational harm to the organization for discriminatory outcomes.

**Requirement (REQ3):** Detection and reporting outcomes for searches do not exhibit systematic disparities by relevant demographic characteristics (e.g., age ranges, skin tone, or other protected characteristics) or by deployment context (e.g., device class or region); significant performance gaps are detectable and do not persist unaddressed.

**Assumptions (ASM):**

- **ASM1**: The organization's missing-child case registry contains accurate, queriable demographic attributes (e.g., age-range, recorded skin-tone category or self-identified race/ethnicity when available) that can be deterministically linked to each reference case ID the software receives for search and post-hoc analysis.
- **ASM2**: Each detection record generated by deployed devices is accompanied by reliable deployment-context metadata (device class/model identifier, geographic region or region-code, timestamp, and camera-quality indicators such as resolution and exposure) so that software can stratify outcomes by device class and region.
- **ASM3**: A representative sample of candidate-sighting outcomes is independently verified by human reviewers within a bounded period after reporting, and those verification labels (confirmed / false / inconclusive) are recorded and made available for centralized evaluation and auditing.

**Specifications (SPEC):**

- **SPEC1**: For every candidate sighting the software must persist a standardized detection record containing: reference case ID, detection timestamp, location (or nearest region-code), device class/model ID, model version ID, raw model outputs (class scores/confidences), link to the image or image hash, and any available demographic attributes from the case registry; these records must be queryable by demographic attribute and deployment-context fields for offline analysis.
- **SPEC2**: The software must run an automated fairness-monitoring pipeline on a regular cadence (e.g., daily or weekly) that computes per-group metrics (at minimum: true positive rate, false positive rate, precision, recall) stratified by each relevant demographic attribute and by deployment context. For each metric and group, the pipeline must (a) enforce a configurable minimum sample size (e.g., N>=50) before reporting comparisons, and (b) perform a statistical test or bootstrap to produce confidence intervals and a significance flag (e.g., p<0.05) for between-group disparities, then persist these results and time series for audit.
- **SPEC3**: If the monitoring pipeline detects a statistically significant disparity that exceeds configured tolerance thresholds for a given metric and group for M consecutive monitoring windows (configurable), the software must automatically (a) generate an incident record linking the disparity evidence and affected model version/training-data identifiers, (b) mark new detections matching the affected group/context for prioritized human review and suppress automated external notifications for those detections until a human reviewer clears them, and (c) notify designated operators via the organization's incident channel with the persisted evidence.
- **SPEC4**: The software must provide authenticated audit APIs and export functions that allow authorized auditors to: (a) retrieve aggregated and raw detection records filtered by demographic and deployment-context fields, (b) sample and retrieve representative example images and associated model attributions/saliency outputs for each group (subject to privacy controls), and (c) obtain model lineage metadata (training dataset identifiers, sampling strategies, preprocessing steps, and model version) necessary to investigate root causes of observed disparities.

#### H4 / REQ4

**Related Goal:** G3

**Loss:** System capabilities are misused by malicious actors or unintended parties to stalk, surveil, or otherwise harm children or families, damaging the organization's credibility and creating safety risks.

**Requirement (REQ4):** Search initiation, access to identifying footage, and receipt of search results are available only to authorized case participants (investigators, the reporting family, and designated organizational staff) for active cases; unrelated third parties and the public do not gain access to identifying search outputs or the ability to initiate searches.

**Assumptions (ASM):**

- **ASM1**: Each authorized case participant has an organizationally assigned, unique identifier and an out-of-band verified contact channel (e.g., organization-controlled email or phone number) that the participant presently controls and can use to complete multi-factor authentication.
- **ASM2**: Case status (active vs. inactive) is determined and updated by authorized organizational staff according to documented procedures, and the authoritative case status record is available to downstream systems within two hours of the staff update.
- **ASM3**: Dashcam devices and intermediary upload services produce and preserve verifiable metadata (timestamp, device ID, and geolocation) for each uploaded footage segment such that metadata can be correlated to case timeframes and candidate sightings.

**Specifications (SPEC):**

- **SPEC1**: Require authentication with at least two factors (e.g., password + OTP or hardware token) for any operation that initiates a search, accesses identifying footage, or receives search results; permit these operations only when the authenticated account is listed as an authorized participant for the specific case in the authoritative case-participant list.
- **SPEC2**: Enforce role-based access control (RBAC) tied to case roles (investigator, reporting family member, designated staff): implement least-privilege rules that map each role to allowed actions (search-initiation, view-identifying-video, receive-results). Deny and generate an auditable alert for any attempted action not permitted by the role mapping.
- **SPEC3**: Before permitting search initiation, access to identifying footage, or delivery of results, consult the authoritative case-status record and allow the action only if the case status is 'active'; if the case is not active or the case-status lookup fails, block the action and record the denial reason, time, and requesting identity in an access audit log.
- **SPEC4**: Treat ML-generated candidate sightings and any identifying footage as sensitive outputs: label each candidate with model confidence and associated metadata (timestamp, geolocation, device ID); deliver unredacted identifying footage or high-resolution stills only to authenticated, authorized participants for active cases and only over encrypted, authenticated channels; when results or previews must be viewable by less-privileged parties, automatically redact or blur identifying features prior to delivery and record the redaction applied in the audit log.

#### H5 / REQ5

**Related Goal:** G5

**Loss:** Investigative teams become overloaded by high volumes of low-quality, duplicate, or untimely alerts, causing delays in responding to genuine leads and inefficient use of limited organizational resources.

**Requirement (REQ5):** Investigators and organizational coordinators receive a manageable number of prioritized, actionable leads per case such that duplicate, low-value, or excessive alerts do not cause investigator workloads to exceed operational capacity or delay timely response to high-priority cases.

**Assumptions (ASM):**

- **ASM1**: The organization provides the system with explicit, current operational capacity thresholds (e.g., maximum alerts per investigator per hour and per case per day) and updates these thresholds when capacity changes.
- **ASM2**: Reference materials for each missing-child case (case ID, at least one frontal face image, approximate last-known location, and time window) are available to the system and are correctly associated with that case.
- **ASM3**: Dashcam devices and network infrastructure deliver candidate sighting reports (images/video), along with capture timestamps and approximate geo-coordinates, to the system within an expected delivery window (e.g., within 60 minutes under normal operating conditions).

**Specifications (SPEC):**

- **SPEC1**: The software must deduplicate candidate sightings by automatically clustering incoming reports that are temporally and spatially proximate and visually similar: it must support configurable temporal (e.g., minutes), spatial (e.g., meters), and image-similarity thresholds and merge clustered reports into a single representative alert that aggregates media and metadata from the grouped reports.
- **SPEC2**: The software must compute a prioritized risk score for each alert using a documented combination of factors (ML model match confidence, recency of sighting, proximity to case last-known location, number of independent reports aggregated, and case criticality flag). Alerts with scores at or above a configurable 'immediate-notify' threshold must trigger immediate investigator notifications; alerts below a configurable 'deliver' threshold must be queued or rate-limited per the configured capacity limits.
- **SPEC3**: The software must enforce configured per-case and per-investigator throughput limits: it must not deliver more than the configured maximum number of alerts to any investigator or any case in a specified time window; when incoming alerts exceed those limits, the software must queue lower-priority alerts, apply backoff or batching, and expose the queued-count and estimated delivery time to coordinators.
- **SPEC4**: Each delivered alert must include an evidence bundle and provenance: capture timestamps, source device ID, geo-coordinates, aggregated media (images/video) or thumbnails, ML model match scores with top-K matched reference images, a summary of duplication/merging rationale, and an immutable audit record (who/when the alert was generated and any subsequent automated or human actions).

## 7. Dashcam manufacturer

### Goals

- **G1**: Ensure device reliability and user safety during normal operation and while running missing-child search features.
- **G2**: Protect user privacy and comply with data-protection regulations to avoid breaches and fines.
- **G3**: Control device resource use and operating costs so devices meet advertised battery, processing, and storage expectations.
- **G4**: Support deployment and coordination with authorities and partner organizations so searches function as contracted and updates can be applied as needed.
- **G5**: Maintain company reputation, limit legal liability, and preserve customer trust.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Dashcams overheat or suffer accelerated battery degradation while performing searches, causing device failure, vehicle damage, safety incidents, increased warranty claims, or product recalls that harm the manufacturer's finances and reputation.

**Requirement (REQ1):** Dashcams remain operational and do not experience overheating, battery failure, or other safety-compromising malfunction during authorized search activities and under expected environmental and usage conditions.

**Assumptions (ASM):**

- **ASM1**: Ambient temperature at the device mounting location remains within the device manufacturer operational range (e.g., −20°C to 60°C) during authorized search activities; the device's internal temperature sensors provide values that correlate sufficiently with ambient conditions to detect excursions outside this range.
- **ASM2**: The vehicle electrical system supplies DC power to the dashcam within expected bounds (approximately 11.0–15.0 V) during authorized search activities, and the device can measure supply voltage and distinguish external/ignition-powered vs. battery-powered states.
- **ASM3**: Authorized search activities are initiated under normal usage behavior (e.g., user or authorized system starts searches while vehicle ignition is ON or while external power is present) and follow predictable duty cycles such that continuous high-intensity search workloads do not routinely exceed roughly 2 hours without observable pauses; the device can observe search start/stop times.

**Specifications (SPEC):**

- **SPEC1**: Continuously monitor internal temperature and supply voltage at least once per minute; if internal temperature >= 60°C or measured supply voltage drops below 11.0 V, automatically reduce ML inference throughput (e.g., reduce frame rate or batch size) by at least 50% or switch to a low-power inference mode; if internal temperature >= 80°C or supply voltage < 10.5 V persistently for 30 seconds, suspend non-essential search activities, persist state for later resume, present a local user alert, and create a timestamped log entry.
- **SPEC2**: Only execute authorized search tasks when the device detects external/ignition power or when battery state-of-charge (SoC) is above a safe threshold (e.g., SoC >= 20%); if the device is running on battery and either battery SoC falls below 20% or battery has been the sole power source for more than 30 continuous minutes, stop or pause search workloads and notify the user, recording the event in logs.
- **SPEC3**: Provide and enforce multiple ML inference modes (minimum: high-accuracy, balanced, low-power). The software must automatically select a lower-power mode when thermal, voltage, or battery thresholds (as defined in SPEC1 and SPEC2) are met, and must record which model variant and mode were used for each detection event. The software must also enforce a maximum continuous high-throughput inference window of 2 hours per session and require at least a 15-minute cool-down period before resuming high-throughput mode.
- **SPEC4**: Generate and store timestamped diagnostic logs for each search session containing: internal temperature readings, supply voltage, battery SoC, inference mode/variant, ML CPU/GPU utilization, session start/stop times, and any throttle/suspend actions. When network connectivity is available, securely transmit these logs to the manufacturer's diagnostics endpoint for post-incident analysis and warranty assessment; additionally present immediate in-device alerts to the user when search activities are suspended for thermal or battery safety reasons.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Identifying images or location data captured by the dashcam are exposed to unauthorized parties, resulting in regulatory fines, class-action suits, and loss of customer trust for the manufacturer.

**Requirement (REQ2):** Unauthorized parties do not gain access to identifying images, location information, or other personally identifying data collected by the dashcam.

**Assumptions (ASM):**

- **ASM1**: The dashcam hardware provides a hardware-backed secure storage (e.g., secure element or TPM) that enforces non-extractability of stored private keys and supports on‑chip cryptographic operations (signing/decryption) without exposing private keys to the environment.
- **ASM2**: Network paths used by the dashcam (cellular and Wi‑Fi) permit end-to-end TLS connections without mandatory TLS interception or replacement of server certificates by intermediaries (i.e., no transparent TLS proxying that injects custom root certificates).
- **ASM3**: Authorized external parties (e.g., investigators, law enforcement) will present verifiable, machine-processable authorizations (for example, digitally signed tokens or warrants via an agreed protocol) when requesting full-resolution images or precise GPS coordinates.

**Specifications (SPEC):**

- **SPEC1**: The software must encrypt all identifying images and associated location metadata at rest using strong encryption (minimum AES-256 or equivalent) with encryption keys bound to the hardware secure storage; the software must never write unencrypted copies to persistent storage and must only decrypt images in volatile memory for authorized operations. (Testable by verifying encrypted storage files and absence of plaintext files and by key-use tests against the secure element.)
- **SPEC2**: The software must use mutual TLS with certificate pinning for all remote transmissions containing identifying images or precise location; by default, the device shall only transmit anonymized thumbnails (max 200x200 pixels, automated face blurring applied) and coarse location (no finer than 1 km). The software shall transmit full-resolution images and exact GPS coordinates only after validating a signed authorization token issued to an authenticated, authorized investigator.
- **SPEC3**: The software must enforce role-based access control and multi-factor authentication for any local UI, local API, or cloud API access to identifying images or precise location data; it must record an auditable log entry for every access containing actor identity, roles, timestamp, data accessed, and presented authorization, and expose log export and alerting interfaces for security review.
- **SPEC4**: The ML pipeline shall output non-reversible feature embeddings or metadata for candidate sightings for use in search/matching and shall not cause automatic disclosure of raw images or exact location based solely on model outputs. The software must associate a confidence score with each detection and require explicit, cryptographically authorized requests before uploading raw images or precise GPS data off-device. (Testable by inspecting exported artifacts and verifying that only embeddings/coarse metadata are sent without a valid authorization token.)

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Coordinated searches consume excessive mobile data or storage, causing users to incur unexpected charges or lose recorded footage; this results in increased support costs, returns, and negative customer feedback for the manufacturer.

**Requirement (REQ3):** Performing coordinated searches does not cause users to incur unanticipated mobile-data charges or to lose existing recorded footage due to storage exhaustion without the user's explicit consent.

**Assumptions (ASM):**

- **ASM1**: The device operating system and cellular stack expose APIs that report current network connection type (Wi‑Fi vs cellular), connection metering status (metered/unmetered), and roaming status to applications in real time.
- **ASM2**: The device filesystems and OS reliably report available local storage in bytes and enforce storage limits so the app can determine whether there is sufficient free space for additional recordings or temporary files.
- **ASM3**: The device environment supports interactive user consent dialogs that the app can present and receive a persistent, verifiable response from (accept/decline), and the user is reachable to respond at the time the app requests consent.

**Specifications (SPEC):**

- **SPEC1**: Before initiating any coordinated-search data transfer over the network, the software shall query the OS for current connection type, metering, and roaming status and shall not transmit over a metered or roaming cellular connection unless the user has explicitly granted consent for that specific transfer or has a preconfigured policy allowing it.
- **SPEC2**: The software shall compute an estimated data-size (in bytes) for each coordinated-search operation (including thumbnails, metadata, and full-resolution uploads) and compare that estimate to either (a) a user-configured per‑billing‑period data quota or (b) an OS-reported remaining data allowance if available; if the estimated transfer would exceed the quota/allowance, the software shall pause the operation and present the user with a clear choice to (i) proceed and accept charges, (ii) restrict transfers to Wi‑Fi only, or (iii) cancel the transfer. The software shall default to not proceeding without affirmative user consent.
- **SPEC3**: To limit mandatory data transfer size, the software shall treat ML-produced candidate sightings as candidates (not confirmed) and, by default, upload only low-resolution thumbnails and metadata for coordinated searches; the software shall require explicit user consent before uploading full-resolution video or multiple contiguous video segments identified by ML for the same candidate sighting.
- **SPEC4**: The software shall check available local free storage (in bytes) before creating temporary files or staging uploads for a coordinated search and shall not automatically delete existing recorded footage to free space. If available free space is insufficient, the software shall (a) notify the user with options to free space (manual delete, move to cloud on Wi‑Fi, or abort search), (b) obtain explicit user consent for any deletion action, and (c) record the user's choice in a local audit log that can be used for support.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Incompatibility with investigators' workflows or inability to deploy updated models prevents the dashcam from delivering usable search results, leading to failed contracts, penalties, and diminished operational partnerships.

**Requirement (REQ4):** Authorized investigators and partner organizations receive relevant sightings and associated footage from the dashcam in a manner and within timeframes that satisfy agreed coordination and operational requirements.

**Assumptions (ASM):**

- **ASM1**: Investigators and partner organizations provide and maintain reachable, authorized endpoints (e.g., server URLs, API keys, contact addresses) as specified in coordination agreements.
- **ASM2**: Network connectivity (cellular, Wi‑Fi, or equivalent) becomes available often enough that queued reports and metadata can be transmitted to investigator endpoints within the delivery and coordination timeframes defined by agreements.
- **ASM3**: Case‑specific legal and privacy authorizations required to transmit footage and identifying metadata to external investigators are valid and in force in the jurisdictions where the dashcams operate.
- **ASM4**: Dashcam hardware and sensors produce usable media and metadata at the time of a candidate sighting: image/video with sufficient resolution/illumination, a timestamp, and location information (GPS or fallback) with accuracy adequate for investigator workflows.

**Specifications (SPEC):**

- **SPEC1**: The software must deliver candidate sightings and associated footage to configured investigator endpoints using a persistent store‑and‑forward queue with retry and exponential backoff; it must record all delivery attempts and, if delivery to a configured endpoint remains unsuccessful beyond the delivery timeframe specified in the coordination agreement, generate and transmit an escalation alert to a configured escalation endpoint.
- **SPEC2**: Each transmitted sighting payload must include machine‑readable fields conforming to the agreed API schema: case ID, sighting ID, detection timestamp, device ID, geographic coordinates with stated accuracy, clip or media link, detection label explicitly marked as a candidate sighting, ML model identifier and version, and detection confidence score; the software must validate the payload against the schema before transmission and reject malformed payloads.
- **SPEC3**: The software must restrict receipt and retrieval of sightings and footage to authenticated, authorized investigator accounts using cryptographic client authentication (e.g., mutual TLS or signed tokens), and must maintain immutable, exportable audit logs recording delivery, access, and administrative actions (including actor identity and timestamps) for compliance and incident review.
- **SPEC4**: The software must support secure over‑the‑air model and software updates: updates must be cryptographically signed and include version and compatibility metadata; the device must verify signatures before activation, perform automated health checks of the new model, automatically rollback to the last verified model on health‑check failure, and report update attempt results and the active model version to the backend within one hour of attempting installation.

#### H5 / REQ5

**Related Goal:** G5

**Loss:** False matches generated by the dashcam lead to wrongful stops, harassment, or public identification of innocent people, causing legal claims, regulatory scrutiny, and severe reputational damage to the manufacturer.

**Requirement (REQ5):** No person is treated by investigators or partner organizations as a confirmed sighting, detained, publicly identified, or otherwise subjected to adverse actions solely because of an automated dashcam match.

**Assumptions (ASM):**

- **ASM1**: Investigators and partner organizations maintain and follow written operational procedures that require documented human review and explicit human confirmation before detaining, publicly identifying, or otherwise subjecting a person to adverse actions based on a candidate sighting.
- **ASM2**: The dashcam system and network deliver the original, uncorrupted image/video and associated metadata (timestamp, GPS, camera ID) to reviewers so that a human can reasonably assess whether the candidate sighting matches the reference.
- **ASM3**: Qualified human reviewers (with required training or role authorization) are available to perform verification of candidate sightings within the operational timeframe required by investigators and partner workflows.

**Specifications (SPEC):**

- **SPEC1**: All automated matches must be labeled, in both machine-readable fields and visible UI, as 'candidate sighting' (or equivalent) and must not be set or promoted to any 'confirmed' status by software alone; the software must ignore ML confidence scores for automatic confirmation and must never trigger downstream actions that rely on a 'confirmed' flag without human confirmation.
- **SPEC2**: The software must require an explicit human confirmation action (distinct UI step) performed by an authenticated, authorized reviewer before enabling any enforcement workflows, generation of public alerts, or sharing of identifying information with third parties; that action must record reviewer identity, timestamp, and a free-text justification.
- **SPEC3**: For each candidate sighting the software must attach and present the original media and metadata (image/video file, timestamp, GPS, camera ID, model version, and model confidence) in a verification interface that: (a) overlays a visible watermark or banner on media indicating 'Candidate — Do Not Act Without Human Verification', and (b) disables export to public channels or automated publication until the human confirmation action in SPEC2 is completed.
- **SPEC4**: The system must create and retain tamper-evident audit logs for every automated match, every notification sent, every access to the candidate media, and every human confirmation/rejection; logs must include actor identity, action, timestamp, and prior match metadata, be queryable for compliance review, and be retained for a configurable retention period.

## 8. ML model vendor / external contractor

### Goals

- **G1**: Deliver reliable detection performance so that legitimate sightings of a missing child are identified and useful to investigators.
- **G2**: Minimize false positives and misidentifications to avoid harm to uninvolved people and to limit legal and reputational exposure.
- **G3**: Ensure privacy-preserving operation and compliance so that identifying footage and location data are handled in ways that meet legal and stakeholder expectations.
- **G4**: Support robust deployability and operation across diverse dashcam hardware and connectivity conditions to avoid deployment failures and unexpected costs.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Legitimate appearances of a missing child in recorded footage are not identified or reported in time, resulting in missed investigative leads, contractual penalties, and reputational damage to the vendor.

**Requirement (REQ1):** Relevant appearances of the missing child captured in dashcam footage under typical deployment conditions are reported to authorized investigators within a timeframe that allows timely follow-up by investigators.

**Assumptions (ASM):**

- **ASM1**: Each recorded video frame includes embedded timestamp and geolocation metadata that are synchronized to real-world time and position to within ±5 seconds and ±10 meters of ground truth.
- **ASM2**: Relevant appearances of the missing child include at least one video frame in which the child's face occupies a contiguous area of at least 32x32 pixels and is occluded on no more than 50% of the face area.
- **ASM3**: Reference materials provided for each missing-child case correspond to the correct child and include at least one clear frontal face image with resolution ≥128x128 pixels.
- **ASM4**: Each dashcam device or its gateway establishes outbound network connectivity to the central reporting service at least once within any 6-hour window under typical deployment conditions, enabling queued uploads within that period.

**Specifications (SPEC):**

- **SPEC1**: When the ML model produces a candidate detection, the software must create and persist a candidate report within 5 minutes that includes: the detection timestamp, source device identifier, GPS coordinates from the associated frame, a short video clip containing ±10 seconds around the detection frame (or full clip if shorter), the single-frame thumbnail used for matching, the ML model's confidence score, the reference-match score(s), and the filename/location of the raw recorded frame.
- **SPEC2**: The software must triage and notify based on measurable scores: if model confidence ≥ 0.90 or reference-match score ≥ defined high-priority threshold, mark the report as high-priority and attempt immediate notification to authorized investigators; if confidence is between 0.50 and 0.90 (or match score between medium thresholds), queue for human analyst review and surface to analysts within 1 hour. The software must retain and retry unsent notifications until delivered or until 24 hours have elapsed, recording retry attempts and final delivery status.
- **SPEC3**: For every candidate report the software must log and retain an auditable record for at least 90 days that contains: raw model inputs (stored frames/clips), model outputs (confidence and match scores), timestamps (detection, report creation, notifications), transmission status history, human review annotations and disposition decisions. These logs must be queryable to produce recall/precision metrics for each case and to support contractual performance audits.
- **SPEC4**: Access to candidate reports and associated raw footage must be restricted to authenticated, authorized investigator or analyst accounts via role-based access control. All report transmissions and authenticated access must use encrypted channels (TLS 1.2 or stronger) and every access or export of a candidate report must be recorded in an access audit log.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Innocent people are mistakenly treated as sightings and publicly identified or investigated without sufficient corroboration, causing privacy violations, legal claims, and reputational harm to the vendor.

**Requirement (REQ2):** People who do not match the missing child are not treated or disseminated as confirmed sightings solely because of an automated prediction; candidate matches provided to investigators must be clearly indicated as unconfirmed and accompanied by supporting contextual evidence before any public dissemination.

**Assumptions (ASM):**

- **ASM1**: Authorized investigators or designated reviewers will retrieve and review received candidate sightings within 24 hours of receipt (as evidenced by investigator-system interaction timestamps).
- **ASM2**: Source cameras/devices or upstream ingestion systems provide accurate capture metadata (geolocation latitude/longitude, UTC timestamp, and a device identifier) embedded in or transmitted alongside each image/video in a machine-readable format that the software can parse.
- **ASM3**: When available from the data source, contextual evidence (a short video clip or a sequence of preceding/following frames, and optional low-resolution face crops) can be transmitted with the capture and will be present at the time the candidate match is reported to the software.

**Specifications (SPEC):**

- **SPEC1**: The software must label every automated detection/match delivered to human reviewers as an explicit 'candidate' or 'unconfirmed' state and must not transition any item to a 'confirmed' or 'sighting' state solely on the basis of an automated model prediction or score.
- **SPEC2**: For each candidate match presented to investigators, the software must attach and display the following supporting contextual fields: capture UTC timestamp, geolocation (lat/lon) and device ID, the short video clip or sequence of frames if available, the model match score and model version identifier, and the identifier of the reference image used for matching; these fields must be included in any investigator-facing API responses or UI records.
- **SPEC3**: The software must enforce role-based access controls and workflow gating so that only users with an explicit 'confirm and publish' privilege can change a candidate's status to 'confirmed' and enable public dissemination; attempting to change status must require entering a justification, attaching corroborating evidence fields (as specified in SPEC2), and creating an auditable log entry with user ID and timestamp.
- **SPEC4**: All investigator-facing interfaces and any exported media or data for a candidate must include a machine-readable and human-visible 'UNCONFIRMED CANDIDATE' warning (for example, a metadata flag plus a visible watermark or banner) and the system must require explicit investigator acknowledgement of that status before allowing export or external sharing actions.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Identifying images or location information are exposed to unauthorized parties or used in ways that violate laws or agreements, leading to regulatory fines, contractual liability, and loss of trust in the vendor.

**Requirement (REQ3):** Identifying images and location metadata collected or generated by dashcams are accessible only to authorized investigative parties and are not disclosed to unauthorized third parties or made publicly available.

**Assumptions (ASM):**

- **ASM1**: An authoritative roster of authorized investigative parties (account identifiers and, where applicable, public cryptographic keys) is maintained by the custodial authority and made available to the dashcam system via an authenticated directory or API; updates to this roster are propagated to the system within a known time window (e.g., 24 hours).
- **ASM2**: Each dashcam device reliably attaches accurate capture metadata to images at the time of capture, including a UTC timestamp and GPS coordinates in a defined schema (e.g., WGS84), such that the software can observe and parse these fields programmatically.
- **ASM3**: The network path between dashcams and the backend does not include untrusted intermediaries that silently intercept or alter payloads (i.e., endpoints can establish end-to-end encrypted channels such that the backend and device can detect if TLS is being intercepted by a proxy).

**Specifications (SPEC):**

- **SPEC1**: The software must enforce authenticated access for all requests to identifying images and precise location metadata: investigator accounts must authenticate (MFA required for investigator role) and the system must perform an access-control decision against the case-specific authorized roster before returning full-resolution images or precise coordinates; unauthorized requests must be denied with an access-failure response and recorded in the audit log.
- **SPEC2**: All identifying images and precise location metadata must be protected in transit and at rest: the system must use end-to-end encrypted transport (TLS) and store these items encrypted at rest using per-case encryption keys or per-resource keys. Keys used to decrypt full data must be accessible only to components that perform the authorization check; key usage and rotation must be verifiable in tests.
- **SPEC3**: When the ML model generates candidate sightings, the software must treat the associated images and precise location metadata as sensitive resources: any user or interface without explicit case-level authorization must receive only redacted representations (e.g., low-resolution thumbnails with faces blurred and coarse location no more precise than a specified radius such as 1 km). Any export or forwarding of full-resolution images or exact GPS coordinates to external services or third parties must require an explicit per-export authorization workflow recorded in the system.
- **SPEC4**: The software must produce tamper-evident, queryable audit records for every access, decryption, or export of identifying images or precise location metadata that include: user identity, authenticated session id, timestamp, resource id, action performed, and stated purpose. Audit logs must be stored append-only and retained according to policy so that tests can demonstrate that every access leaves a corresponding immutable log entry.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Model deployments cause excessive resource use or incompatibilities on deployed dashcams (e.g., loss of other recordings, device instability, or unexpected recurring costs), resulting in product returns, support costs, and damage to the vendor's reputation.

**Requirement (REQ4):** Search operations initiated on a dashcam do not cause loss of previously recorded footage, prevent the device from performing its normal functions, or require users to incur unexpected device-related costs (such as unanticipated mobile-data charges or premature hardware replacement) beyond typical usage expectations.

**Assumptions (ASM):**

- **ASM1**: The dashcam firmware/OS exposes accurate, queryable system metrics (available persistent storage, current CPU utilization, available RAM, battery level, and I/O latency) and enforces process scheduling priorities such that a foreground recording process can preempt or be prioritized over background tasks.
- **ASM2**: Network interfaces on the dashcam (cellular and Wi‑Fi) report connection properties (connection type, metered vs unmetered, roaming status) reliably, and data transfers over cellular/roaming can incur carrier charges according to those reported properties.
- **ASM3**: The dashcam maintains a persistent rolling-recording area or reserved storage quota for primary recordings that can be observed by software (e.g., reported reserved buffer size or protected partition) and that other processes will not be allowed to overwrite that reserved area by the device's storage management policies.

**Specifications (SPEC):**

- **SPEC1**: Before starting or writing any search-related data, the software shall read the device-reported reserved_recording_space and current_free_space and must not perform writes that would reduce current_free_space below reserved_recording_space; if free space < reserved_recording_space, the software must abort or defer the search and surface a clear message to the user. (Test: attempt search with free_space < reserved_recording_space and verify no recording data is deleted or overwritten.)
- **SPEC2**: The ML inference and ancillary search processing shall run within configurable resource limits: maximum sustained CPU utilization <= 40% of total CPU, maximum additional RAM usage <= 50% of available RAM, and maximum sustained disk write I/O additional latency <= 20 ms; the software must continuously monitor these metrics and immediately throttle or pause inference if any limit is exceeded or if the recording process shows increased write latency or dropped frames. (Test: simulate high load and verify inference throttles/pauses and recording continuity is preserved.)
- **SPEC3**: The software shall detect connection properties before transferring data and must not transfer more than 5 MB of data over a network reported as metered or roaming without explicit, logged user consent; bulk uploads shall be queued for unmetered/Wi‑Fi connections or require explicit opt-in. (Test: set network to metered/roaming and attempt a large upload; verify upload is blocked/consent requested and upload proceeds only on consent or unmetered connection.)
- **SPEC4**: Search-related temporary files and model caches shall be stored in an isolated, non‑overlapping storage location (separate partition, fenced directory, or ephemeral filesystem) and all writes that could affect recorded footage must be atomic and checksummed; on software crash, update, or restart the software shall verify checksums and restore or preserve original recording files, logging any integrity failures and refraining from deletion of original footage. (Test: induce crash during search and verify that pre-existing recordings remain intact and are checksum-verified on restart.)

## 9. System integrators / software developers

### Goals

- **G1**: Protect identifying data and maintain regulatory compliance and organizational reputation.
- **G2**: Ensure timely and reliable delivery of sighting reports to authorized investigators.
- **G3**: Prevent misuse of automated detections and minimize false-positive driven harm or workload.
- **G4**: Maintain consistent, stable behavior across heterogeneous dashcam hardware and power/storage constraints.
- **G5**: Respect user concerns about mobile-data usage, battery drain, and storage consumption to avoid opt-outs and complaints.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Unauthorized parties gain access to identifying images, location data, or personally identifying metadata, causing legal/regulatory penalties, reputational damage, and increased remediation workload for integrators.

**Requirement (REQ1):** Unauthorized parties do not gain access to identifying images, location information, or personally identifying metadata collected, stored, or transmitted as part of the missing-child search process.

**Assumptions (ASM):**

- **ASM1**: Dashcam devices have access to a reliable external time/source (e.g., GPS or NTP) so that capture and transmission timestamps can be verified to be within +/- 10 seconds of true time.
- **ASM2**: Public key infrastructure and certificate revocation services used by the dashcam and backend (trusted CAs, OCSP/CRL) are available and return valid responses so endpoints can obtain and validate TLS and recipient encryption keys.
- **ASM3**: Physical custody and tamper protections of dashcam devices are maintained by authorized vehicle operators between image capture and upload, so devices are not routinely stolen, opened, or physically accessed by unauthorized parties.

**Specifications (SPEC):**

- **SPEC1**: Encrypt all identifying images, location data, and personally identifying metadata at rest using strong, industry-standard cryptography (e.g., AES-256-GCM) with keys managed by a hardware-backed key store or separate key management service; implement automated tests that verify ciphertext cannot be decrypted without the key and that key access requires authorized roles.
- **SPEC2**: Transmit identifying images, location data, and PII only over authenticated, end-to-end encrypted channels such that only explicit authorized recipient keys can decrypt payloads; the software must validate recipient keys/certificates and fail transmission if validation (including revocation checks) does not succeed; include automated tests that simulate invalid/ revoked certificates and ensure transmission is blocked.
- **SPEC3**: Enforce role-based access control with multifactor authentication for any interface that can access identifying images or location metadata; authorization decisions must be logged, sessions should expire after configurable idle time, and access attempts (successful or denied) must produce immutable audit records whose integrity is verifiable (e.g., hash chain) to support later forensic review.
- **SPEC4**: Default to data minimization and redaction: when ML inference produces candidate sightings, the system shall store and transmit only non-identifying derived features or redacted/low-resolution thumbnails to unverified or general-purpose recipients; full-resolution identifying images and exact location metadata may be retained or released only after explicit authorized approval, and the software must record that approval event; include tests that verify thumbnails are blurred/obfuscated to a defined metric and that full images are inaccessible without recorded authorization.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Investigators do not receive relevant sightings in time for the footage to be actionable, resulting in missed opportunities to locate a child and increased post-incident liability and support burden for developers.

**Requirement (REQ2):** When the dashcam and coordinating systems have network connectivity sufficient for transmission, authorized investigators receive relevant sighting reports and accompanying contextual information within a timeframe in which the associated footage remains operationally useful.

**Assumptions (ASM):**

- **ASM1**: Dashcam devices retain captured raw footage for at least 24 hours after capture (a configurable retention_window), so footage referenced by a candidate sighting remains locally available until that expiry.
- **ASM2**: Cellular or Wi‑Fi connectivity sessions with at least 200 kbps average throughput and minimum continuous duration of 30 seconds occur often enough for the device to transmit a minimal sighting package before the local footage retention_window expires.
- **ASM3**: Authorized investigators or investigator intake systems monitor the designated reporting channels and are able to receive and review incoming candidate sighting reports within 60 minutes of the report being delivered to the intake endpoint.

**Specifications (SPEC):**

- **SPEC1**: For every candidate sighting the software must include machine-observable metadata: capture timestamp (ISO8601), device identifier, GPS coordinates (latitude/longitude with ±m accuracy if available), video frame index or frame-range, estimated footage expiry time (based on the device retention_window), and the byte-size of the associated payload.
- **SPEC2**: The software shall queue and prioritize outbound sighting reports by earliest estimated footage expiry and implement deterministic retry/backoff transmission logic: attempt immediately when connectivity is detected, if transmission fails retry after 30 seconds, then double the interval on each subsequent failure up to a maximum of 5 attempts or until the reported footage expiry time is reached; each attempt and final status must be recorded in a transmission log.
- **SPEC3**: When bandwidth is constrained, the software must produce and transmit a prioritized, compact contextual package that fits within the available throughput: a small set of representative still frames (1–5), object bounding boxes for detections, ML model confidence scores and top-3 candidate match scores against the case reference, and an explicit label of 'candidate sighting' (not confirmed). The package must include the model confidence values so investigators can triage results; the software must not treat low-confidence outputs as confirmed sightings.
- **SPEC4**: The system must deliver reports to investigator endpoints using authenticated, authorized channels and maintain an auditable trail: require token-based authentication for endpoint delivery, include an integrity checksum (e.g., SHA‑256) with each report, record ISO8601 timestamps for report generation, transmission attempts, and acknowlegements, and retain transmission and access logs for at least 90 days for post-incident review.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** High rates of false positives cause innocent people to be subject to investigation or public attention, eroding trust in the system and generating heavy support, legal, and remediation work for integrators.

**Requirement (REQ3):** Automated detections are not treated as confirmed sightings on their own; people who do not match the missing child are not reported to investigators or third parties as confirmed sightings solely because of an automated prediction.

**Assumptions (ASM):**

- **ASM1**: Qualified human reviewers (investigators or trained operators) will access and review candidate detections generated by the system within a defined review window (e.g., 24 hours) after the detection is available to the review queue.
- **ASM2**: Captured sensor data associated with detections includes usable metadata: a timestamp accurate within ±5 seconds of the capture event and geolocation accurate within ±30 meters, so that reviewers can reliably assess location/time of a candidate sighting.
- **ASM3**: Reference images and case metadata supplied for each missing-child case correspond to the correct child and include at least one frontal face image or clear body/clothing description that a human reviewer can use to compare against candidate detections.

**Specifications (SPEC):**

- **SPEC1**: The software must label all ML-generated events as 'candidate sighting' (or equivalent) in the user interface and persistent records; it must never change that label to 'confirmed sighting' without an explicit manual confirmation action by an authenticated human reviewer.
- **SPEC2**: The software must block any automated workflow that would transmit a 'confirmed sighting' notification to investigators, law enforcement, media outlets, or other third parties; transmissions originating from automated detections are permitted only to internal review queues or accounts with reviewer role permissions.
- **SPEC3**: For each candidate sighting the software must persist and present to reviewers: the original media frames, ML outputs (confidence score, bounding boxes, match-similarity metrics), model identifier and version, and the capture metadata (timestamp, geolocation, camera ID); all of these must be logged in an auditable record when a human reviewer confirms or rejects the sighting.
- **SPEC4**: The software must require an explicit recorded action from an authorized reviewer to change a candidate to confirmed; that action must capture reviewer identity, timestamp, and a short justification, and only after this action may the system send a 'confirmed sighting' alert to external investigators or third parties. Until confirmation, any external-facing exports must include a prominent 'candidate' label and withhold or redact personally identifying details unless allowed by a reviewer.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Inconsistent or resource-intensive behavior on some dashcam models causes device instability, loss of recorded footage, degraded primary recording functionality, or large numbers of device returns and support cases.

**Requirement (REQ4):** Across the supported range of dashcam hardware models and typical power/storage states, the missing-child search feature does not cause persistent device instability, loss of previously recorded footage, or inability to perform the device's core driving-recording functions during normal operation.

**Assumptions (ASM):**

- **ASM1**: During execution of the search feature, the device power source (vehicle/USB/battery) remains within the manufacturer's specified operating voltage range and does not undergo unplanned abrupt power losses beyond normal ignition cycles.
- **ASM2**: At the time the search feature starts, the device has at least 100 MB of free, writable storage space in a filesystem that is not corrupted and that supports atomic file creation/rename operations.
- **ASM3**: Device operating temperature and ambient conditions remain within the manufacturer's specified operating temperature range for the duration of the search operation (i.e., no thermal shutdown or hardware-level throttling occurs while the feature runs).

**Specifications (SPEC):**

- **SPEC1**: Resource monitoring and graceful degradation: the software must continuously monitor available storage, CPU utilization, memory, and input power. If free storage falls below 50 MB, search-attributable CPU utilization exceeds 85% for more than 5 seconds, available process memory falls below 30 MB, or input power drops below the device-specific safe threshold, the software must suspend or pause search activities and release nonessential resources within 2 seconds while ensuring the primary recording process remains running.
- **SPEC2**: Recording protection and file handling: the search feature must run at lower OS scheduling priority than the primary recording process, must not acquire exclusive locks on the camera device or existing recording files, and must write all temporary and search-related files to a separate directory or partition. The feature must never overwrite or delete existing recordings without an explicit atomic transaction and backup; on any write failure or filesystem error it must abort the operation and leave existing recordings unmodified.
- **SPEC3**: Inference and processing limits: ML inference and image-processing tasks must be rate-limited and scheduled so they consume no more than 50% of available CPU cores or GPU processing averaged over any 10-second window. If processing would exceed that limit, the software must reduce work (e.g., lower frame-sampling rate) or defer/offload processing (only if network bandwidth/latency checks pass). ML work must not block the real-time recording I/O thread.
- **SPEC4**: Crash/recovery and diagnostics: the software must checkpoint or flush in-progress temporary outputs at least every 2 seconds, implement a watchdog to detect hung or crashed search tasks and restart them safely, and on next startup after abnormal termination perform a filesystem integrity check and verify that previously recorded footage is intact before resuming normal recording or allowing searches. Any integrity failures must be reported to logs/telemetry and preserved for diagnostics rather than being auto-deleted.

#### H5 / REQ5

**Related Goal:** G5

**Loss:** Search operations trigger unexpected mobile-data charges, excessive battery drain, or large storage consumption, prompting user complaints, opt-outs, or disabling of the feature and increasing developer support demand.

**Requirement (REQ5):** Search operations and any associated data transfers, storage usage, or processing invoked by the dashcam do not impose unexpected or undisclosed mobile-data, battery, or storage costs on device owners beyond what is communicated and consented to prior to initiating a coordinated search.

**Assumptions (ASM):**

- **ASM1**: The device operating system reliably reports current network connectivity type and metered/unmetered status (e.g., cellular vs. Wi‑Fi and whether the carrier marks the connection as metered) via APIs the software can read.
- **ASM2**: The device operating system reliably reports battery level and charging state via APIs the software can read, and those reported values reflect actual device battery state during search operations.
- **ASM3**: A device owner or authorized user is presented with and is able to respond to on‑device consent and configuration prompts before initiating a coordinated search (i.e., the user can view and set data/battery/storage preferences and grant or deny consent).

**Specifications (SPEC):**

- **SPEC1**: Before beginning any coordinated search that may use network, battery, or persistent storage, the software shall present an explicit consent UI that (a) summarizes estimated data, battery, and storage impacts for the proposed operation, (b) allows the user to select and save preferences (e.g., 'Wi‑Fi only', 'Allow cellular up to X MB', 'Only while charging'), and (c) requires an affirmative opt‑in to proceed when predicted usage exceeds the saved preferences.
- **SPEC2**: The software shall enforce a network‑aware transfer policy: when the OS reports a metered (cellular) connection, the software will restrict outgoing transfers to metadata and low‑bandwidth artifacts and must not transfer more than a configurable per‑search mobile‑data cap (default 5 MB) unless the user explicitly overrides; transfers exceeding the cap must be queued and retried only when an unmetered connection is available or when explicit user consent is recorded.
- **SPEC3**: By default the software shall perform ML inference on‑device and only upload minimal artifacts: compressed thumbnails and metadata for candidate sightings. Full‑resolution images or continuous video may be uploaded only if (a) user consent was obtained per SPEC1, or (b) an unmetered connection and sufficient battery/charging state are detected. Image uploads must be compressed to a configurable maximum size (default 200 KB per image) and the system must enforce a configurable per‑case upload count limit (default 10 images) unless the user explicitly increases limits.
- **SPEC4**: The software shall record, surface to the user, and make available to integrators detailed accounting for each search operation: actual bytes transmitted over each interface, storage bytes consumed, and estimated battery drain attributed to the operation. If predicted or measured usage will exceed the consented limits or configured quotas (e.g., storage per case, mobile‑data cap), the software shall notify the user and pause or stop further data transfers until the user authorizes continuation.

## 10. Cloud service providers / data center operators

### Goals

- **G1**: Protect confidentiality and integrity of hosted data and prevent unauthorized access to identifying images and location metadata.
- **G2**: Maintain availability and performance of platform services for all customers, avoiding degradation due to hosted workloads.
- **G3**: Avoid legal and regulatory liability by ensuring hosted content and processing comply with applicable laws (including laws concerning child exploitation materials and data protection).
- **G4**: Ensure predictable resource usage and cost exposure, preventing unexpected operational costs or capacity strain from customer workloads.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Identifying images or location metadata processed or stored by the dashcam service are exposed to unauthorized parties, causing regulatory fines, customer churn, and reputational damage to the provider.

**Requirement (REQ1):** Identifying images and location information processed or stored on the provider's infrastructure are not accessible to unauthorized parties.

**Assumptions (ASM):**

- **ASM1**: Physical access to the data center racks and storage hardware is controlled by the provider (badges, cameras, guards) and access events are logged by facility systems; those facility access logs are available to the provider's operators via an API for audit within 24 hours of the event.
- **ASM2**: The cloud provider's key management service (KMS) and hardware security modules (HSMs) correctly enforce key separation between tenants, prevent unauthorized extraction of master or customer keys, and expose key usage/rotation status and metadata via provider APIs usable by the service.
- **ASM3**: Network isolation mechanisms (VPCs, private subnets, tenant network segmentation, internal routing) prevent arbitrary Internet-originated traffic from reaching storage nodes containing images and location metadata; the provider exposes networking configuration and flow logs to the service/operator for verification and auditing.

**Specifications (SPEC):**

- **SPEC1**: All images and associated location metadata stored on provider infrastructure must be encrypted at rest using customer-specific KMS-managed keys; the software must ensure every storage object records the key identifier and must not store or log plaintext cryptographic key material. Backups, snapshots, and replicas must be created only if they are encrypted with the same or an approved KMS key.
- **SPEC2**: All transport of images and location metadata between clients, service components, and storage must use mutually authenticated, strong TLS (or equivalent) using provider-issued client certificates or equivalent identity tokens; the software must reject connections that do not present valid authentication and must use internal-only endpoints for storage access.
- **SPEC3**: The software must enforce fine-grained authentication and authorization for any access to images or location metadata (role-based access control or attribute-based policies), record an immutable audit log for every access attempt (successful or failed) including requester identity, timestamp, resource identifier, operation performed, and bytes/fields accessed, and must generate an alert when access patterns deviate from configured baselines (e.g., bulk export, unusual source location).
- **SPEC4**: During ML inference or other processing, the software must decrypt image pixels and raw location metadata only in ephemeral memory within a designated secure execution environment (e.g., enclave or dedicated processing instance), must not write decrypted images or raw location data to persistent storage or standard logs, must purge in-memory copies immediately after processing, and must store any derived artifacts (embeddings, feature vectors) encrypted and labeled as sensitive.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Dashcam-related workloads produce sustained resource consumption or traffic patterns that degrade availability or performance for other tenants, resulting in SLA breaches and operational disruption.

**Requirement (REQ2):** Workloads attributable to the dashcam service do not cause sustained degradation of availability or performance for other hosted services or tenants.

**Assumptions (ASM):**

- **ASM1**: The cloud infrastructure enforces configured per-tenant resource quotas and isolation for CPU, memory, storage IOPS and network egress such that actual instantaneous and sustained consumptions do not exceed configured limits by more than 10% under sustained workloads.
- **ASM2**: The provider exposes per-tenant resource and traffic telemetry (CPU, memory, storage IOPS, network egress, and instance counts) via APIs or metrics streams with a maximum reporting latency of 60 seconds and measurement accuracy within ±10%.
- **ASM3**: Requests to provision additional capacity (scale-out, increase bandwidth/quota) via the provider API complete within 5 minutes when permitted by account quotas, or the API returns a visible failure or quota-exceeded response within that same time window.

**Specifications (SPEC):**

- **SPEC1**: The dashcam service must sample its own per-tenant resource usage (CPU, memory, storage IOPS, network egress) at least once every 30 seconds and compare observed usage to configured tenant quotas. If any resource remains above its configured quota for 60 continuous seconds, the service must reduce consumption for that resource to within quota within 30 seconds by applying throttling, queuing, or shedding noncritical work, and must emit a logged alert containing the resource metric, duration, and remediation action.
- **SPEC2**: When observed usage reaches 80% of allocated capacity for any resource, the service must attempt to provision additional capacity via the provider API. If provisioning does not succeed within 5 minutes (per ASM3), the service must automatically apply predefined degradation strategies until capacity is available: delay or batch uploads, reduce video upload bitrate by at least 50%, reduce capture or inference frequency by at least 50%, and limit concurrent cloud inference requests per tenant to a configurable low concurrency (e.g., 1–2). All degradations must be logged with timestamps and reason.
- **SPEC3**: The service must enforce network egress smoothing and priority-based batching: it must ensure the average per-tenant network egress does not exceed the configured egress limit over any 5-minute sliding window by using token-bucket or leaky-bucket enforcement. If instantaneous bursts would exceed the bucket, the service must queue or drop lowest-priority data (e.g., non-urgent telemetry) and record the dropped/queued volumes and priority decisions in logs/metrics.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** The provider becomes legally exposed or subject to enforcement action because hosted data meets statutory definitions of illegal content (for example, prohibited child exploitation material) or violates data-protection or data-residency laws.

**Requirement (REQ3):** Data and processing activities associated with the dashcam service comply with applicable criminal, data-protection, and data-residency laws, such that hosted collections do not include material that would subject the provider to criminal liability or regulatory enforcement.

**Assumptions (ASM):**

- **ASM1**: Uploaded dashcam footage and associated images can contain visual content involving minors that, under one or more applicable jurisdictions, meets statutory criteria for prohibited child exploitation material (for example, nudity or sexualized context as defined by local law).
- **ASM2**: Each upload includes reliable provenance metadata (for example: device IP geolocation at time of upload, device-registered country, or explicit capture-location metadata) that can be used to determine the jurisdiction where the footage was collected or first uploaded.
- **ASM3**: Competent authorities and authorized requestors can deliver legally valid preservation, takedown, or disclosure orders to the provider via authenticated channels, and those orders will specify content identifiers or sufficiently precise metadata to identify affected items.

**Specifications (SPEC):**

- **SPEC1**: For every uploaded file, run an automated content-safety classifier that produces a confidence score for 'prohibited child exploitation material'. If score >= 0.90, the software must immediately (a) move the file into a quarantined, access-restricted storage location that is not served to downstream search/indexing pipelines, (b) block any external sharing or CDN publication of the quarantined copy, and (c) generate an alert and immutable audit record for the compliance/legal team containing the content identifier, score, provenance metadata, and timestamp.
- **SPEC2**: If the classifier score is in [0.50, 0.90), the software must mark the item 'suspected-prohibited' and (a) restrict access to a small, auditable set of authorized human reviewers, (b) ensure reviewers see the classifier confidence and provenance metadata, and (c) require an explicit human review decision within 2 hours to either (i) clear the item and move it back to searchable storage or (ii) escalate it to quarantine as in SPEC1. All reviewer actions must be logged with user identity and timestamps.
- **SPEC3**: Use provenance metadata to enforce data-residency rules: for each uploaded item determine jurisdiction J from metadata; store the canonical raw footage only in provider data centers or cloud regions designated for J (no cross-region replication outside permitted regions), and tag the item with the applied region policy. If jurisdiction cannot be determined, route the item to an encrypted, access-restricted staging region and reject any global replication until jurisdiction is resolved. These routing decisions and final storage locations must be verifiable in an audit log.
- **SPEC4**: Upon receipt of an authenticated legal preservation/takedown/disclosure order that references content identifiers or unambiguous provenance metadata, the software must (a) place specified items on legal hold (preventing deletion/modification/automatic purge), (b) produce a chain-of-custody record and exportable report of access logs for those items, (c) notify the provider's legal/compliance group within 1 hour, and (d) if the order requires production, enable export only to authenticated, authorized endpoints with watermarking and a restricted retention/usage policy. Execution of the order and all actions taken must be logged immutably.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Unexpected or abusive usage patterns from the dashcam system cause unplanned operational costs, capacity shortfalls, or require emergency scaling, harming the provider's financial predictability and planning.

**Requirement (REQ4):** Resource consumption and network traffic generated by the dashcam service remain within agreed contractual usage patterns and do not impose unanticipated costs or emergency capacity requirements on the provider.

**Assumptions (ASM):**

- **ASM1**: The number of active dashcam devices sending data to the provider under the contract does not exceed the contracted maximum active-device count (e.g., N devices) during normal operation; transient exceedances are rare and bounded.
- **ASM2**: Per-device reporting frequency and data volume follow the contracted usage distribution (for example: median reports/day = R_med, 99th-percentile reports/day = R_99); sustained region-level spikes above the contracted 99th-percentile are exceptional events rather than continuous behavior.
- **ASM3**: The cloud provider publishes tenant-level resource-usage and billing metrics (ingress bytes, request rates, CPU/memory quota usage, and current billing accrual) via APIs with at most Z minutes latency and stated accuracy within ±A%, enabling timely programmatic assessment of current consumption against contractual limits.

**Specifications (SPEC):**

- **SPEC1**: Enforce hierarchical rate limits: the software must enforce per-device upload/report caps (default: max_uploads_per_device = R_d per minute) and per-tenant caps (default: max_uploads_per_tenant = R_t per minute) at ingress. When a cap is reached, the system must (a) reject additional immediate uploads with a standard throttling response (e.g., HTTP 429), (b) place lower-priority items into a bounded retry queue with exponential backoff, and (c) emit an audit log entry for each throttled event. These limits and behaviors must be configurable and verifiable by automated tests that simulate rates above and below R_d and R_t.
- **SPEC2**: Perform on-device and edge pre-filtering with ML-confidence-aware upload rules: each candidate-detection sent to the cloud must include model confidence. The device software must only upload full-resolution assets when confidence >= C_high (default 0.90). For C_low <= confidence < C_high (default C_low = 0.60), upload only compressed thumbnails and metadata (timestamp, location, model confidence, detector type). For confidence < C_low, do not upload image/video; instead upload only low-cost metadata or suppress reporting entirely. These thresholds must be configurable and testable by feeding detections with known confidence values and verifying the transmitted payload types and sizes.
- **SPEC3**: Adapt traffic shaping and sampling based on provider metrics: the cloud-side software must poll the provider's usage/billing API at least once every T minutes (default T = 5). If projected 24-hour consumption exceeds contracted quota by more than X% (default X = 10%), automatically reduce global upload sampling rate by at least Y% (default Y = 50%), apply stricter per-device caps, and emit an operator alert with the predicted overage amount and timestamps of applied mitigations. All decisions and metric inputs must be logged for reconciliation and their correctness verifiable in integration tests that mock provider metrics.
- **SPEC4**: Detect and mitigate abusive or unexpected usage patterns: the system must run server-side anomaly detection that flags sources exceeding K detections in M minutes (default K = 100, M = 5) or exhibiting burst patterns inconsistent with contracted behavior. Upon detection, automatically throttle the offending source to a safe baseline rate, optionally suspend uploads from that source after repeated violations, mark the source for manual review, and emit a billing-impact estimate. The anomaly detector configuration, detections, and enforcement actions must be observable and reproducible in test harnesses that simulate abusive patterns.

## 11. Mobile carriers and hotspot providers

### Goals

- **G1**: Protect network capacity and control operating costs associated with high-volume or bursty data transfers.
- **G2**: Maintain compliance with privacy laws and lawful-access obligations when transporting personally identifying data.
- **G3**: Avoid being exploited as a channel for unauthorized data exfiltration or bulk transfer of unrelated content.
- **G4**: Limit reputational and support costs arising from customer privacy complaints, regulatory inquiries, or high-profile incidents involving transported content.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Large or poorly timed search-related uploads/downloads cause sustained congestion or degraded service for the provider's other customers, increasing churn and operational costs.

**Requirement (REQ1):** Search-related transfers do not cause sustained degradation of network performance or availability for other customers on the same network segments.

**Assumptions (ASM):**

- **ASM1**: Network congestion on a provider's shared radio or access segment produces observable degradations (increased round‑trip latency, measurable packet loss, and reduced achievable throughput) that client devices can detect within a 60‑second measurement window.
- **ASM2**: Mobile carriers and hotspot providers apply per‑subscriber or per‑segment bandwidth controls (caps, throttling, or priority queuing) that produce consistent, measurable limits on sustained throughput over hour‑scale windows.
- **ASM3**: Provider network usage exhibits repeatable temporal patterns (e.g., diurnal peak/off‑peak behavior) that can be inferred from historical telemetry or crowd‑sourced measurements to predict lower‑load windows for scheduling bulk transfers.

**Specifications (SPEC):**

- **SPEC1**: The software shall continuously measure local network metrics (e.g., round‑trip time, packet loss, and throughput) and enforce adaptive rate limiting on search‑related uploads/downloads: if measured latency increases by >100 ms above a rolling baseline or packet loss exceeds 2% for 5 continuous minutes, reduce transfer rates for non‑urgent data to <= 30% of historical baseline throughput for that client until metrics recover.
- **SPEC2**: When a carrier/hotspot provides real‑time congestion, quota, or scheduling APIs, the software shall query those APIs before initiating large transfers and obey returned limits or recommended windows; if an API indicates explicit per‑subscriber caps or disallows bulk transfers, the software shall defer or throttle transfers to comply and log the provider directive and compliance action.
- **SPEC3**: The software shall classify and prioritize data by urgency: (a) for ML‑flagged candidate sightings with detection confidence >= 0.95, immediately transmit only compact, compressed metadata and a low‑resolution thumbnail (<= 100 KB); (b) for lower‑confidence detections or raw/high‑volume evidence (video, high‑res images), queue and schedule transfers during predicted low‑load windows or when measured network metrics satisfy the thresholds in SPEC1. The software must record detection confidence, payload size, and transfer timing for auditing.
- **SPEC4**: The software shall monitor the aggregate contribution of its transfers to local link utilization and abort or further throttle search‑related transfers if its sustained usage appears to exceed 40% of estimated available capacity on the shared segment for more than 10 minutes. The software shall emit logs/telemetry describing utilization, the actions taken (throttle/abort/defer), and timestamps for provider or operator audit.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** The provider transports personally identifying images or precise location information without clear authorization, exposing the provider to privacy complaints, regulatory fines, or legal requests.

**Requirement (REQ2):** Personally identifying images and precise location information are only transmitted over the provider's network when the transmission is authorized by the account holder or by a documented lawful investigator request, and the provider can distinguish authorized from unauthorized transmissions.

**Assumptions (ASM):**

- **ASM1**: Each subscriber account has a stored consent status for transmissions of personally identifying images and for transmission of precise location; that consent status is accessible to the provider software via the provider's account-management API and is returned as a machine-readable field tied to the account identifier.
- **ASM2**: Lawful investigator requests are issued to the provider through a documented electronic channel that includes a signed request token containing an agency identifier, case identifier, timestamp, and expiration; the provider can obtain and use the issuer's public-key material or equivalent to verify those signatures.
- **ASM3**: When an account holder or authorized investigator grants authorization for a specific transmission, that authorization is represented as a tamper-evident, machine-verifiable token or header (bound to account/device and payload type or case ID) that is presented with the transmission and is observable by the provider's network systems.

**Specifications (SPEC):**

- **SPEC1**: Before sending any image the software classifies as potentially personally identifying or before sending precise geolocation (latitude/longitude to within the provider's definition of 'precise'), the software must query the account-management API and require either (a) an explicit account-holder authorization token for that account and payload type, or (b) a valid signed lawful-request token. If neither valid token is present and verified, the software must block transmission of the sensitive data payload.
- **SPEC2**: For any incoming claimed lawful-request token, the software must validate the token signature, verify the issuer against a maintained authorized-agency list, check the token's case identifier and expiration, perform revocation verification if available, and record the verification outcome (including issuer ID, case ID, timestamp, and verification result) in an audit log. If validation fails, the software must not release personally identifying images or precise location based on that token.
- **SPEC3**: The software shall run an image-analysis component that outputs a sensitivity label, a confidence score, and model-version metadata for each captured image. Any image whose sensitivity label indicates 'personally identifying' at or above a configurable confidence threshold must be treated as sensitive: transmission of the image or of embedded/extracted precise location data is prohibited unless a valid authorization token (account-holder or lawful-request) is present. The software must include the model output (label, confidence, version) in the transmission decision log for audit.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Malicious actors repurpose the dashcam data channel to exfiltrate large volumes of unrelated user data or contraband content, increasing the provider's exposure to abuse and legal risk.

**Requirement (REQ3):** Network traffic identified as originating from dashcam search operations does not carry unrelated user data or high-volume payloads inconsistent with authorized search activity.

**Assumptions (ASM):**

- **ASM1**: Dashcam search operations are routed over identifiable network endpoints or channels (e.g., distinct APN, VLAN, VPN endpoint, dedicated TCP/UDP port range, or a verifiable HTTP(S) Host/SNI) such that carriers can map observed flows to 'dashcam search' origin without decrypting application payloads.
- **ASM2**: Authorized dashcam search activity produces predictable, low-volume traffic patterns (e.g., periodic small feature vectors, thumbnails, metadata records) with typical per-upload size and rate bounds that are stable enough to define testable thresholds.
- **ASM3**: Carriers can lawfully and technically observe flow-level metadata (connection start/stop times, total bytes transferred, packet size distribution, ports, SNI, and other unencrypted headers) for the dashcam-associated channel and can act on that metadata in near-real-time.

**Specifications (SPEC):**

- **SPEC1**: The dashcam client software must restrict outgoing 'search operation' network connections to an allowlist of authorized server endpoints and ports; any attempt by local processes to send data labeled for the search channel to non-allowlisted endpoints must be blocked and logged with timestamp, destination, and byte count.
- **SPEC2**: The dashcam client must serialize and transmit only permitted payload types for search activity (e.g., feature vectors, low-resolution thumbnails, timestamps, location metadata). The client must enforce per-payload maximum size and per-connection throughput limits; attempts to transmit payloads exceeding these limits must be rejected and trigger a local audit log entry.
- **SPEC3**: The dashcam client must attach verifiable origin metadata to each search-operation flow (signed device ID, operation ID, and content-type tag) in an unencrypted header or channel field observable by network operators; the client must record a local record of the signature, operation ID, and transmitted byte counts for later cross-checking.
- **SPEC4**: Carrier-side monitoring software must inspect flow-level metadata for flows identified as dashcam-search, enforce configured thresholds (per-connection byte limit, per-minute throughput, and maximum connection duration), and automatically throttle, block, or quarantine flows that exceed thresholds or use non-permitted protocols; each enforcement action must generate an alert containing flow identifiers, observed byte counts, and the reason for enforcement.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Privacy incidents or ambiguous transmissions generate regulatory investigations and customer support burdens because the provider cannot attribute or investigate what content was transported and why.

**Requirement (REQ4):** Providers can correlate transported dashcam search traffic with the originating account or device and the authorization context so they can investigate and respond to privacy or regulatory inquiries.

**Assumptions (ASM):**

- **ASM1**: The carrier or hotspot provider maintains up-to-date subscription/account records that deterministically map network-level identifiers (e.g., IMSI/eSIM identifier, SIM ICCID, assigned IP address ranges, or device-provisioned provider token) to a customer account and that these mappings can be queried by authorized investigators.
- **ASM2**: Network infrastructure and intermediary systems on the provider path (core network elements, NATs, carrier-grade firewalls) record and retain transport metadata (source IP, NAT mapping, cell-site/tower identifier, APN/hotspot identifier, and timestamps) in logs without irreversible anonymization for at least the investigation retention window.
- **ASM3**: Devices using the dashcam system transmit their search traffic over networks that do not consistently obfuscate or replace application-layer provenance tokens (for example, by mandatory anonymizing VPNs) such that the provider-verifiable identifiers and signatures embedded in payloads remain available to the carrier for correlation.

**Specifications (SPEC):**

- **SPEC1**: For every network transmission related to a dashcam search event, the software MUST include a provider-verifiable authorization token in the payload header. The token must be cryptographically signed (by the device or an authority) and contain: a provider-assigned account identifier or mapping token, the missing-child case identifier, the authorization scope/role, issuance timestamp, and an expiration timestamp. The software MUST refuse to attach raw image/video content to transmissions that do not present a valid, unexpired token.
- **SPEC2**: The software MUST record and transmit a structured audit record with each candidate-sighting message that includes: local timestamp (UTC), device unique identifier (device serial or device-provisioned ID or hashed SIM ID), GPS location (if available) with accuracy estimate, local network interface identifier (e.g., SIM/eSIM id or Wi‑Fi MAC hash), a globally unique message/audit ID, and a digital signature over the record. Each audit record MUST be persisted locally until an explicit acknowledgement from the server is received and retransmitted on next connectivity if not acknowledged.
- **SPEC3**: For any automated detection transmitted, the software MUST include provenance metadata: model identifier and version, detection confidence score(s), detection class/type, a deterministic hash of the extracted image features or of the transmitted image snippet (not the full raw image if privacy policy requires), and a flag indicating automated vs human-confirmed. The software MUST label each transmission as either 'automated_candidate' or 'human_confirmed' to make the reason for transport explicit to downstream investigators.
- **SPEC4**: The software MUST implement an export and query interface (local on-device and server-side) that, given a time range or message/audit ID and appropriate authorization, returns the signed payload and associated audit record required by providers to correlate traffic to accounts. The interface MUST support cryptographic verification of signatures and MUST log every export request with requester identity, time, and the returned message IDs for auditability.

## 12. Members of the public / bystanders captured in footage

### Goals

- **G1**: Preserve personal privacy and avoid unwanted identification from incidental recordings.
- **G2**: Avoid being wrongly treated as a suspect or person of interest because of an automated match.
- **G3**: Prevent secondary uses or long-term retention of images that enable surveillance or tracking.
- **G4**: Limit unauthorized access, disclosure, or downstream sharing of identifying footage and location information.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G2

**Loss:** A bystander is misidentified as the missing child and reported to investigators, leading to stops, questioning, harassment, or reputational harm.

**Requirement (REQ1):** People who do not match the missing child are not reported to authorities as confirmed sightings or prioritized for enforcement actions solely because of an automated prediction.

**Assumptions (ASM):**

- **ASM1**: Trained human reviewers (investigators or delegated analysts) will review each candidate sighting submitted by the system within 24 hours and have authority to mark a sighting as confirmed before any enforcement action or external dissemination.
- **ASM2**: Dashcam devices supply accurate location and time metadata: GPS coordinates with median error ≤ 10 meters and timestamps synchronized to UTC within ±5 seconds, and this metadata is available to the software for every recorded clip.
- **ASM3**: Reference materials for a missing-child case (photographs, reported age/date, unique case ID) are correct for the intended subject and are delivered to the system with associated metadata (date taken and claimed age) so reviewers can assess visual changes over time.

**Specifications (SPEC):**

- **SPEC1**: The software must label all ML-generated matches as 'candidate sighting' (not 'confirmed') in every interface and must not automatically send candidate sightings to external enforcement channels or set enforcement-priority flags without an explicit human reviewer action that marks the sighting as 'confirmed'.
- **SPEC2**: For each candidate sighting the software submits to reviewers, it must deliver the original video segment, cropped candidate frames, GPS and timestamp metadata, the ML model similarity score, and a short machine-generated explanation of key matching features; the software must record reviewer identity, decision (confirm/reject/needs-more-info), decision timestamp, and any reviewer-entered justification in an auditable log before any escalation.
- **SPEC3**: The software must implement de-duplication and rate-limiting so that repeated detections of the same person within a configurable spatial-temporal window (default: 100 meters / 30 minutes) are grouped as a single candidate and must prevent automated prioritization of a candidate for enforcement based solely on ML similarity score—only a human reviewer may assign priority and must provide a recorded justification.
- **SPEC4**: The software must restrict dissemination of unconfirmed candidate imagery: internal authorized reviewers may access unredacted footage, but any transmission outside the authorized review environment (including to external agencies or public alerts) must either (a) redact/blur faces of non-suspected bystanders or (b) require an explicit reviewer authorization recorded in the audit log to share unredacted imagery.

#### H2 / REQ2

**Related Goal:** G1

**Loss:** Images of bystanders are retained and later searched or linked across cases, enabling ongoing identification and loss of anonymity in public spaces.

**Requirement (REQ2):** Incidentally captured images of bystanders that are not demonstrably relevant to an active, authorized missing-child investigation are not retained or made available for future searches or cross-case linking.

**Assumptions (ASM):**

- **ASM1**: Each captured frame/event produced by the dashcam includes observable metadata (timestamp, device ID, and GPS/location when available) that is delivered to downstream processing components alongside image pixels.
- **ASM2**: Authorized investigators or designated law-enforcement agents will, when an image is demonstrably relevant, submit a case identifier and explicit retention authorization through an authenticated channel within a bounded time window after capture (e.g., before the configured automatic purge).
- **ASM3**: Active authorized missing-child investigations are associated with a machine-readable case identifier and a defined scope (time ranges, geographic bounds, reference images) that can be provided to the system to determine whether particular captures fall inside the investigation scope.

**Specifications (SPEC):**

- **SPEC1**: Images and derived biometric data for persons not explicitly marked as relevant to an active authorized case must be deleted or irreversibly purged from searchable storage within a configurable retention_period (default: 30 days) from the time of capture; the system must provide an automated process that removes those items and produce a deletion proof log entry recording image ID, capture timestamp, and deletion timestamp.
- **SPEC2**: When an ML model produces a candidate match between a captured image and a case reference, the software must: (a) label the result as a 'candidate' (not confirmed), (b) store any intermediate biometric templates or feature vectors only in ephemeral, case-scoped storage encrypted-at-rest, (c) grant access to candidate images and templates only to authenticated, authorized investigator accounts, and (d) require an explicit human verification action (recorded with verifier ID and timestamp) before converting the candidate into a persistently retained record or linking it across cases.
- **SPEC3**: The system must not create or maintain a global, persistent index of biometric identifiers that enables cross-case linking of bystanders; instead it must either (a) store per-case, ephemeral, non-global feature representations that are deleted when the case closes or retention expires, or (b) store only non-searchable hashes/records that cannot be used to match images across different cases. The enforcement mechanism and deletion of per-case artifacts must be auditable.
- **SPEC4**: Retention or exception actions that preserve images of bystanders beyond the standard purge must require a valid case identifier and an authorization token from an authorized account; the software must validate the token, record the retention_reason, retention_authorizer_id, and retention_expiry, and refuse retention requests lacking valid authorization.

#### H3 / REQ3

**Related Goal:** G4

**Loss:** Identifying footage or associated location metadata is accessed or shared with unauthorized parties (e.g., advertisers, third-party apps, or public leaks), causing privacy breaches, stalking, or commercial exploitation.

**Requirement (REQ3):** Identifying images and location information of bystanders are not accessible to parties who are not authorized to participate in the specific, documented missing-child investigation.

**Assumptions (ASM):**

- **ASM1**: For each missing-child investigation, an authoritative, machine-readable list of authorized participants (including roles and verifiable credentials or public keys) is delivered to the system by the investigating agency and can be validated by the system.
- **ASM2**: Captured footage ingested by the system includes associated capture metadata (timestamp and location/GPS coordinates) that is accurate to within the granularity required for the investigation and is available to the software at ingestion.
- **ASM3**: Network and storage infrastructure deliver and preserve ingested footage and metadata with integrity (i.e., files are not corrupted or silently altered) such that cryptographic checksums or signatures computed at capture can be verified after transfer.

**Specifications (SPEC):**

- **SPEC1**: The software must enforce per-case access control: before returning any image or any precise location metadata linked to bystanders, verify the requester’s credentials and role against the case-specific authorized-participant list and deny access if the requester is not listed for that case.
- **SPEC2**: When any footage or derived image is delivered to recipients who are not authorized participants for the specific case, the software must remove or obfuscate identifying visual features of bystanders (e.g., faces, tattoos) and strip or coarsen precise location metadata; obfuscation and location granularity must be configurable and applied by default.
- **SPEC3**: ML outputs that indicate detected persons (target or bystanders) must be accompanied by detection metadata (bounding boxes, labels, confidence scores); the software must treat all non-target humans as protected by default and only include unredacted visual data or precise location when an authorized participant explicitly requests access and the request is recorded.
- **SPEC4**: All accesses, delivery attempts, and de-redaction/unobfuscation actions for identifying images or precise location metadata must be logged with requester identity, case id, timestamp, and purpose; these logs must be tamper-evident and retained according to policy, and the software must alert administrators on repeated unauthorized access attempts.

#### H4 / REQ4

**Related Goal:** G3

**Loss:** Data derived from dashcam footage are used to infer sensitive attributes or to build searchable indices of bystanders (e.g., to trace attendance at events), leading to discrimination, chilling effects, or misuse by authorities or private actors.

**Requirement (REQ4):** Footage and derived data are not used to infer, label, or create searchable records of bystanders' sensitive attributes or association patterns for purposes unrelated to the authorized missing-child search.

**Assumptions (ASM):**

- **ASM1**: Authorized missing-child search requests are accompanied by verifiable, machine-readable authorization tokens issued by a trusted authority that explicitly list the case ID, permitted processing operations (e.g., candidate sighting matching), and token expiration; the software can validate the token's authenticity against the issuing authority.
- **ASM2**: Requesting investigators/operators will not supply external bystander identity labels, sensitive-attribute labels, or association graphs as input to the system for searches; any such labels or association data would only originate from the system's own processing outputs (i.e., no authoritative external attribute metadata is provided).
- **ASM3**: Footage and its accompanying sensor metadata (timestamps, GPS) do not contain pre-attached machine-readable markers that encode bystander-sensitive attributes or persistent cross-case person identifiers; therefore any such markers would have to be produced by the software itself to exist in stored outputs.

**Specifications (SPEC):**

- **SPEC1**: Authorization enforcement: The software must validate incoming authorization tokens and permit processing only for operations explicitly listed in a valid token. If a request specifies any operation that infers, labels, indexes, or searches by sensitive attributes (e.g., race, religion, political views, sexual orientation, health) or that builds association/attendance graphs of bystanders, the software must reject the request with an error, refuse to execute the operation, and record the rejection in the audit log.
- **SPEC2**: Data minimization and storage prohibition: The software must not compute, persist, or export labels or structured records that represent bystanders' sensitive attributes or that create persistent person identifiers that link appearances of the same bystander across multiple unrelated cases. Embeddings or features used exclusively for matching to the authorized case's reference images may be used transiently in-memory or stored encrypted and scoped to the single case, and must be automatically deleted within 30 days or upon case closure—whichever is sooner. Storage schemas and databases must have explicit schema-level prohibition of fields for sensitive-attribute labels and cross-case person IDs; attempts to add such fields must be blocked and logged.
- **SPEC3**: ML-model and inference controls: Only ML models explicitly approved for child-match scoring (matching candidate sightings to the provided reference images) may be invoked during processing of an authorized case. The runtime must enforce a model allowlist and block any model invocation that would output sensitive-attribute predictions or association/co-occurrence graphs. All model invocations must be logged with model identifier, input case ID, and a record that the model is from the approved allowlist; any attempt to register or call a blocked model must raise an alert and be recorded.
- **SPEC4**: Query API and index restrictions plus auditing: The search and query APIs must not accept queries that specify sensitive-attribute filters or that request lists of bystander occurrences independent of a specific active missing-child case. The system must prevent creation of searchable indices keyed by bystander appearance, bystander ID, or co-occurrence relationships. Every creation, modification, or query that could create or expose association data or attribute labels must be recorded in an immutable audit trail; automated audits must run at least daily to detect attempted or successful creation of attribute labels or association indices and trigger administrative review and retention/fix actions.

## 13. Privacy and data-protection regulators

### Goals

- **G1**: Ensure personal data collection, use, and retention are limited to what is necessary and lawful (data minimization, purpose limitation, retention limits).
- **G2**: Prevent unauthorized disclosure or misuse of identifying images and location data collected or derived by the dashcam system.
- **G3**: Maintain the ability to audit, investigate, and demonstrate compliance with data-protection obligations and citizens' rights.
- **G4**: Ensure that any sharing or transfer of personal data, including cross-border transfers, complies with applicable legal requirements and approvals.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Excessive or indefinite retention of dashcam footage and metadata unrelated to an active, authorized missing-child search, causing unlawful processing and noncompliance with retention and purpose-limitation rules.

**Requirement (REQ1):** Footage and associated personal-data derived from dashcam recordings that do not pertain to an active, authorized missing-child search are not retained or made available for further processing beyond the legally permitted retention period and are not used for other purposes.

**Assumptions (ASM):**

- **ASM1**: An authoritative case-management source (e.g., police/child-missing registry) provides machine-verifiable case metadata (case ID, active/inactive flag, permitted retention duration, jurisdiction) via an authenticated API or signed message that the dashcam system can fetch and validate.
- **ASM2**: Each recorded video file delivered to the system contains reliable, machine-readable timestamp and geolocation metadata (UTC timestamp and GPS coordinates) that reflect when and where the footage was captured.
- **ASM3**: Requests from authorized entities to extend retention, grant access, or require deletion are delivered through a well-defined verifiable channel and include digitally verifiable authorization tokens or signatures that the system can validate against the authoritative source.

**Specifications (SPEC):**

- **SPEC1**: The software shall implement and enforce a jurisdiction-aware default retention scheduler that automatically and irreversibly deletes (or cryptographically renders unrecoverable) raw footage and any derived personal-data for recordings not associated with an active authorized missing-child case once the applicable retention period expires; each deletion action must be recorded in an audit log with file identifier, deletion timestamp, and retention rule applied.
- **SPEC2**: The software shall only mark footage as associated with an active authorized missing-child search when it has validated a signed case authorization (case ID matching file metadata or an explicit linkage), or when an ML-generated candidate sighting is subsequently confirmed by an authorized human reviewer; footage not so validated or confirmed remains subject to the default retention schedule.
- **SPEC3**: ML-generated candidate detections must be stored with explicit metadata labeling them as 'candidate' (including model version, timestamp, confidence score, and bounding metadata); the software shall not extend retention beyond default retention solely based on the ML prediction—any retention extension must require a validated authorization token or recorded human confirmation; all ML outputs and subsequent reviewer decisions must be recorded in the audit trail.
- **SPEC4**: The software shall enforce case-scoped access control: only authenticated principals presenting a valid, case-specific authorization may retrieve footage or derived personal-data associated with that case; every access attempt (successful or denied), authorization validation, retention-extension, and deletion must be logged with actor identity, presented authorization token ID, timestamp, case ID, and action, and logs must be exportable for regulatory audit.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Unauthorized parties gain access to identifying images or location information from searches, resulting in privacy violations, harm to individuals, and regulatory enforcement actions against operators.

**Requirement (REQ2):** Unauthorized parties do not gain access to identifying images or location information collected or derived during missing-child searches.

**Assumptions (ASM):**

- **ASM1**: Dashcam devices and backend hardware provide and expose hardware-backed secure storage and remote attestation (e.g., TPM/secure element) so the operator can verify device identity and that keys are present and untampered.
- **ASM2**: Network infrastructure and operator-controlled certificate authorities enforce encrypted, authenticated channels (e.g., TLS with operator-managed certs) between dashcams, backend services, and investigator endpoints, preventing undetected man-in-the-middle interception.
- **ASM3**: Accounts and endpoints used by investigators and other authorized personnel are governed by organizational identity controls (MFA, per-user credentials) and are not intentionally shared with unauthorized parties; compromise incidents are reported to the operator within a defined timeframe.

**Specifications (SPEC):**

- **SPEC1**: All access to identifying images, image embeddings, and location metadata requires an authenticated session and an explicit, role-based authorization check; unauthorized requests must be rejected with no identifying data returned and with an auditable denial reason.
- **SPEC2**: All stored images, derived embeddings, and location metadata must be encrypted at rest with keys managed by an operator-controlled KMS/HSM; cryptographic keys usable for decryption must only be usable by software components running inside a trusted execution environment or with strong attestation, and key usage events must be logged.
- **SPEC3**: For users without privileged clearance, the software must return only redacted, low-resolution thumbnails and non-identifying metadata; retrieval of full-resolution images or precise location data requires an auditable multi-step authorization workflow (e.g., two-person approval or case-link verification) and explicit user intent, and the software must enforce that workflow.
- **SPEC4**: The software must produce immutable audit logs for every search, match, and data-access event (including requester identity, timestamp, device ID, query parameters, and what was returned), retain logs for a regulator-defined period, and implement anomaly detection and rate-limiting to throttle or block unusually frequent downloads or queries to prevent exfiltration.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Regulators cannot obtain reliable records of processing activity (what data was collected, shared, or deleted), preventing effective investigation of complaints and enforcement of legal obligations.

**Requirement (REQ3):** Regulators can obtain complete, time-stamped records sufficient to show which identifying footage and associated metadata were collected, accessed, shared, retained, or deleted for any specific missing-child search so compliance with applicable law can be verified.

**Assumptions (ASM):**

- **ASM1**: Network-connected cameras, edge devices, and backend servers synchronize their clocks to a common authoritative time source (e.g., NTP/UTC) such that timestamp drift between any two involved components is ≤5 seconds under normal operation.
- **ASM2**: Any external recipients of footage or metadata (e.g., law enforcement partners, cloud processors) retain machine-readable records of received items (file identifier, receipt timestamp, recipient account, and retention/deletion actions) and can produce those records upon legitimate regulator request within 30 calendar days.
- **ASM3**: Cameras and storage systems attach and preserve a persistent, globally-unique identifier and capture metadata (device ID, geo-location if available, capture timestamp) to each footage file at the moment of capture, and intermediate network elements do not alter or strip those identifiers during transfer.

**Specifications (SPEC):**

- **SPEC1**: Maintain an immutable, append-only audit log covering every event that affects identifying footage or associated metadata (including collection/capture, automated ML detection, human review/access, exports/sharing, retention-policy application, and deletion). Each audit entry must include: ISO 8601 UTC timestamp, object persistent identifier, event type, actor identity and role, operation result, and a machine-readable reason/legal basis when applicable.
- **SPEC2**: When the ML pipeline processes footage and produces a candidate/identifying result, record a structured inference record that includes: model identifier and version, inference timestamp, input footage identifier(s), preprocessing pipeline version, raw and normalized confidence scores, decision thresholds used, and whether a human reviewer subsequently confirmed or overturned the result (with reviewer id and timestamp).
- **SPEC3**: Provide an authenticated, auditable export API that, given a missing-child search identifier or reference image ID, returns the complete, time-ordered set of audit records and associated metadata and footage identifiers in a machine-readable format (e.g., JSON/NDJSON). Exports must include cryptographic hashes of referenced footage files and be produced within 30 calendar days of a valid regulator request.
- **SPEC4**: Protect audit log integrity using tamper-evident mechanisms (cryptographic signatures, chained hashes, or append-only ledger). Publish verification material or provide a verification endpoint so regulators can confirm that returned audit records are authentic and unmodified. Retain audit logs and indexes for at least the regulatory retention period and support queries by search ID, footage identifier, device ID, actor, and time range.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Identifying footage or personal data is transferred to jurisdictions without a lawful transfer basis or regulatory authorization, causing breaches of cross-border data-transfer rules and potential sanctions.

**Requirement (REQ4):** Identifying footage or personal data collected during searches is not exported or otherwise transferred to jurisdictions unless a lawful transfer basis or required regulatory authorization for that transfer is in place.

**Assumptions (ASM):**

- **ASM1**: Every piece of collected footage or personal-data record includes reliable origin metadata at capture time: device or camera identifier, geo-coordinates (or country-level location), timestamp, and uploader account or organizational owner information that can be used to determine the data's origin jurisdiction.
- **ASM2**: An authoritative, externally maintained mapping exists that can resolve destination network endpoints, IP addresses, cloud-region identifiers, or organizational identifiers to legal jurisdictions (country/territory) and is available to query with sufficiently low latency and up-to-date accuracy for transfer-decision purposes.
- **ASM3**: When a lawful transfer basis or regulator authorization is required for cross-border transfers, the regulator or authorized legal entity issues determinable, machine-verifiable authorizations (for example, signed certificates or tokens) that explicitly list the permitted origin jurisdictions, destination jurisdictions, scope (case IDs or data categories), and expiration, and those authorizations are accessible to the system at decision time.

**Specifications (SPEC):**

- **SPEC1**: Before initiating any export of identifying footage or personal data to an external endpoint, the software shall: (a) determine the data's origin jurisdiction using the record's origin metadata; (b) determine the destination jurisdiction by resolving the target endpoint via the authoritative mapping; and (c) allow the export only if a valid, unexpired, machine-verifiable lawful-transfer authorization exists that explicitly permits transfers from the origin jurisdiction to that destination for the given case or data category. If no such authorization is present or verification fails, the software must block the transfer and return a specific error code.
- **SPEC2**: For any proposed cross-border transfer of footage flagged by the ML component as containing a potential missing child, the software shall require a documented human authorization step before export: a human reviewer must verify the match, confirm that the applicable lawful transfer basis or regulator authorization applies to this specific case, and record reviewer identity, timestamp, justification, and the identifier of the authorization certificate. The software must deny automated export until this human authorization record is present and linked to the transfer attempt.
- **SPEC3**: The software shall produce an immutable audit record for every attempted export (successful or blocked) that includes: data identifier (pseudonymized or hashed), origin jurisdiction, destination jurisdiction, resolution method used for jurisdiction mapping, presence and identifier of lawful-transfer authorization (or absence), human reviewer id if applicable, timestamp, and transfer result. The software shall prevent forwarding these audit records to jurisdictions different from the origin unless a valid lawful-transfer authorization for audit-data export exists, and shall provide an API for regulators to retrieve audit records within the origin jurisdiction for compliance review.

## 14. Legal professionals and courts

### Goals

- **G1**: Understand and rely on the reliability and accuracy of person-recognition outputs when assessing evidence.
- **G2**: Obtain a clear, auditable chain of custody and provenance for footage and derived artifacts used as evidence.
- **G3**: Understand systematic errors and demographic performance differences so bias or discriminatory impacts can be evaluated.
- **G4**: Ensure that evidence is lawfully obtained and restricted to authorized use to prevent privacy violations and unlawful disclosure.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** An innocent person is identified as the missing child based solely on the system's automated match, leading to wrongful investigation, detention, or reputational harm.

**Requirement (REQ1):** Automated recognition outputs are not used by investigators or adjudicators as definitive proof of identity; any action that can materially affect a person's liberty or legal status must be based on additional human-reviewed or independently corroborated evidence.

**Assumptions (ASM):**

- **ASM1**: Investigators and adjudicators operate under agency or court policies that prohibit taking actions that materially affect a person's liberty or legal status based solely on automated outputs from the dashcam system.
- **ASM2**: At least one independent corroborating source (for example, a live human eyewitness, additional independent surveillance footage, or an official identity record) will be accessible to investigators for a reported candidate sighting within seven days of the system reporting that sighting.
- **ASM3**: Reference images and case metadata uploaded into the system by reporting parties correctly correspond to the missing child and include uploader identity and upload timestamp so that investigators can assess provenance.

**Specifications (SPEC):**

- **SPEC1**: Labeling and display: Every automated face-match result presented to users must be prominently labeled as 'candidate sighting — not confirmed' (or equivalent), show the model similarity/confidence score and model version, and display the reference image and captured image side-by-side for human review.
- **SPEC2**: Provenance and audit logging: For each candidate sighting the software must create an immutable record that includes detection timestamp, camera ID, geolocation (if available), captured frame(s), model confidence score(s), model version and matching parameters, and any subsequent human reviewer identity, review timestamp, and review outcome; these records must be searchable and exportable.
- **SPEC3**: Human-approval gating: The system must prevent any automated action that could materially affect a person's liberty or legal status (including generating official 'confirmed' identifications or sending law-enforcement notifications that trigger detention procedures) until a named human reviewer authorizes the action and attaches at least one independent corroborating evidence item to the sighting record.
- **SPEC4**: Investigator guidance and reporting: For each candidate sighting the system must produce an exportable report template that includes a clear disclaimer that automated matches are not definitive, a checklist of required corroborating-evidence types, and a summary of the model's confidence and known limitations; the UI must require an investigator acknowledgement of this report before allowing case-status changes labeled as 'confirmed' or equivalent.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Footage or derived outputs lack trustworthy provenance or handling records, rendering them inadmissible or unreliable as evidence in court.

**Requirement (REQ2):** For each image, clip, or derived result presented for investigative or legal purposes, a persistent record of its origin, capture time, and handling events is preserved and made available to authorized legal parties for review.

**Assumptions (ASM):**

- **ASM1**: Each capture device (dashcam) reliably embeds or exposes a stable, globally unique device identifier (device ID) that can be observed by the software at time of ingestion.
- **ASM2**: Device clocks are synchronized to a trusted time source (e.g., GPS or NTP) such that the device-reported capture timestamp is within 5 seconds of real-world time, and the device includes that timestamp in the captured file metadata.
- **ASM3**: Authorized legal parties have access to or can obtain the public verification material (e.g., public keys or verification certificates) needed to independently verify digital signatures and integrity proofs produced by the system.

**Specifications (SPEC):**

- **SPEC1**: On ingestion of every image, video clip, or ML-derived result, the software must create and persist an immutable metadata record that includes: a system-assigned global artifact identifier, the source device ID, the device-reported capture timestamp, capture location if present, a cryptographic hash of the raw data (SHA-256 or stronger), the ingestion timestamp, and a digital signature over the record produced with the system's private key. The record must be stored in append-only storage and be retrievable by artifact identifier.
- **SPEC2**: The software must maintain a verifiable chain-of-custody audit log for each artifact. Each log entry must record: actor identifier (authenticated user or system component), actor role, action type (ingest, access, export, modify, deleteAttempt), action timestamp, and the artifact hash after the action. Audit log entries must be append-only, cryptographically protected (signed or chained hashes), and exportable for legal review.
- **SPEC3**: Provide an evidence-package export function that, upon authenticated and authorized request, produces a machine-readable package containing the original media, the immutable metadata record, the full chain-of-custody log, and all cryptographic signatures. The package format and verification steps must be documented; the system must include a verification manifest that enables independent integrity checks using the published public verification material.
- **SPEC4**: For any ML-derived output used in investigations, the software must attach provenance metadata linking the output to its source media and processing context: source artifact identifier(s), frame index or timestamp ranges, preprocessing steps and parameters, ML model identifier and version, model input hash, model output confidence score(s), and processing timestamp. This provenance must be included in the immutable record and be retrievable and exportable with the evidence package.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** The recognition system disproportionately misidentifies people from particular demographic groups, producing biased evidence and exposing agencies to discrimination claims.

**Requirement (REQ3):** Known limitations and measured performance differences of the recognition system across demographic groups are documented and disclosed to investigators and legal counsel whenever footage or automated outputs are relied upon in an investigation or proceeding.

**Assumptions (ASM):**

- **ASM1**: An independently validated evaluation dataset exists that contains ground-truth demographic labels for the demographic groups relevant to the jurisdictions where the system is deployed, and that dataset is accessible to the organization performing performance measurements and audits.
- **ASM2**: Investigators and legal counsel receive case materials electronically through the system's delivery channels and those channels support attaching and delivering supplemental documentation (for example PDF or machine-readable reports) together with footage and automated outputs.
- **ASM3**: The vendor or operating organization performs periodic model evaluations that produce timestamped performance reports stratified by demographic group and stores those reports in a retrievable location that can be provided to investigators or legal counsel on request.

**Specifications (SPEC):**

- **SPEC1**: For every exported automated detection, match, or candidate sighting delivered to investigators or legal counsel, the software must attach or link a machine-readable evaluation report for the currently deployed model version that includes: model identifier (version/hash), evaluation date, the evaluation dataset identifier or reference, and measured metrics (at minimum: precision, recall, false positive rate, false negative rate) for each demographic group present in the evaluation; inclusion of the report must be recorded in an audit log with timestamp and recipient identifier.
- **SPEC2**: Whenever footage or automated outputs are displayed, exported, or printed for investigative or legal use, the software must present a human-readable disclosure summarizing that measured performance varies across demographic groups, list the largest measured disparities (e.g., highest and lowest group-specific false positive/negative rates), provide recommended mitigations (for example: require human corroboration), and record delivery of this disclosure with timestamp and recipient identifier.
- **SPEC3**: The software must label all automated identifications and matches in user interfaces and exported reports as 'candidate sightings' (or an equivalent term making clear they are not confirmed identifications) and must not mark any automated match as confirmed; any action workflow that treats a match as confirmed must require an explicit human verification step that is recorded in the audit log with identity and timestamp.
- **SPEC4**: The software must provide an authenticated audit/download endpoint or packaged export that authorized investigators or legal counsel can use to retrieve the full evaluation artifacts for the deployed model version (machine-readable per-group metrics, links or references to evaluation datasets, and evaluation methodology); all accesses and downloads must be logged with user identity, timestamp, and the model version retrieved.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Identifying images or location data are accessed or disseminated by unauthorized parties, causing privacy violations, harassment, or legal liability that must be adjudicated.

**Requirement (REQ4):** Identifying images and associated location information are not accessible to individuals or entities lacking legal authorization for the specific investigation and remain unavailable for public or unintended distribution.

**Assumptions (ASM):**

- **ASM1**: An authoritative, queryable registry of legal authorizations (e.g., warrants or court orders) exists and contains machine-verifiable fields for case ID, authorized data types (images, location), authorized parties, validity period, and a digital signature that the system can fetch and validate.
- **ASM2**: Legal professionals and court staff who are entitled to access hold digital credentials (for example, organization-issued certificates or government SSO accounts) issued by a recognized identity provider, and a public key infrastructure (including certificate revocation information) is available for the system to validate those credentials.
- **ASM3**: The system can reach external services needed to evaluate authorizations in real time (e.g., the authorization registry and PKI revocation lists) with sufficient reliability during access attempts, or those services provide a cached/verifiable representation of authorization state that the system can use when live checks are temporarily unavailable.

**Specifications (SPEC):**

- **SPEC1**: Before releasing any identifying image or associated precise location data, the software must require an authenticated requester and must validate a presented digital legal authorization by querying the authorization registry and verifying the registry fields (case ID, authorized data types, authorized parties, validity period) and the registry's digital signature; if validation fails or the requested data is outside the authorization scope, the software must deny access.
- **SPEC2**: All identifying images and associated location metadata must be stored encrypted at rest and transmitted only over authenticated, integrity-protected channels; encryption keys for decrypting identifying data must be accessible only after successful authorization validation and must be rotated and logged per key-management policy so that unauthorized accounts or revoked authorizations cannot decrypt previously stored data.
- **SPEC3**: The software must enforce least-privilege access controls and role-based permissions: by default provide only redacted or blurred thumbnails and coarse, non-identifying location metadata to unauthenticated or non-authorized users; log every access attempt (successful or failed) to identifying data with requester identity, authorization used, timestamp, case ID, and action in an immutable audit record; and support immediate programmatic revocation of access rights so that revoked authorizations cannot subsequently retrieve identifying images or locations.

## 15. Insurance companies

### Goals

- **G1**: Minimize payouts and litigation costs resulting from incorrect identifications or wrongful actions triggered by the dashcam system.
- **G2**: Limit liability, regulatory fines, and compensation costs arising from unauthorized disclosure of personal or location data.
- **G3**: Reduce claims escalation and associated costs by ensuring timely, actionable reporting of legitimate sightings to investigators.
- **G4**: Prevent fraudulent or unauthorized use of the search feature that could create false incidents, unnecessary investigations, or increased claim frequency.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Incorrect person-recognition results lead to innocent people being treated as sightings, prompting unnecessary investigations, civil claims against vehicle owners or manufacturers, and insurer payouts for legal defense or settlements.

**Requirement (REQ1):** People who do not match the missing child should not be reported to investigators or treated as confirmed sightings solely because of an automated prediction.

**Assumptions (ASM):**

- **ASM1**: Human reviewers or investigators are available and responsible for adjudicating candidate sightings and will not initiate official investigative actions based solely on an automated prediction without an explicit human confirmation step.
- **ASM2**: For the majority of candidate-detection events (e.g., >70% under normal operating conditions), the camera and environment produce media in which the subject's face or other distinguishing features meet a minimum observable quality (for example, a face region of at least 80x80 pixels with less than 30% occlusion) so a human reviewer can make a reliable match/no-match decision.
- **ASM3**: Reference materials provided for a missing-child case by authorized parties include at least one clear frontal face image and basic descriptive metadata (approximate age, height range, distinguishing marks) sufficient for a human reviewer to compare against captured media.

**Specifications (SPEC):**

- **SPEC1**: All automated detections from the person-recognition model must be stored and displayed only as 'candidate_sighting' (or equivalent unconfirmed status) and must not be marked or transmitted as a 'confirmed_sighting' by the software without an explicit human reviewer action that changes the status.
- **SPEC2**: The software must require a documented human-review workflow before any candidate sighting is forwarded to external investigators as a confirmed lead: present the captured media, reference images, model confidence score, and image-quality metrics; require the reviewer to choose 'confirm' or 'reject'; record reviewer identity, timestamp, and rationale; and only upon an explicit 'confirm' action change the status to confirmed and permit transmission to investigators.
- **SPEC3**: The software must suppress automatic forwarding of candidate sightings to investigators when model confidence is below a configurable high-confidence threshold (e.g., system default), and instead route such low-confidence candidates to a 'needs additional review' queue; suppression behavior and threshold values must be configurable and logged.
- **SPEC4**: The system must maintain an immutable audit trail for each candidate sighting that includes: the raw captured media (or reference to it), model outputs and confidence scores, image-quality metrics, all human-review actions (identity, decision, timestamps, notes), and all outgoing notifications to investigators, and must make this audit trail available for post-incident review and dispute resolution.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Identifying images or location histories recorded by dashcams are exposed to unauthorized parties, resulting in regulatory fines, compensation claims, and increased liability for covered entities that insurers must underwrite or defend.

**Requirement (REQ2):** Unauthorized parties do not gain access to identifying images, location information, or other personal data that could lead to regulatory liability or compensation claims.

**Assumptions (ASM):**

- **ASM1**: Each deployed dashcam includes a tamper-resistant hardware security module (HSM/secure enclave/TPM) that can generate, store, and use cryptographic keys and perform signing/encryption operations via documented local APIs; the HSM resists simple software-level extraction of keys.
- **ASM2**: Dashcams and the backend cloud services have sufficient intermittent network connectivity such that encrypted uploads, key/credential revocation signals, and remote-wipe commands can be delivered within a defined window (e.g., 48 hours) under normal operating conditions.
- **ASM3**: Authorized investigators, operators, and account holders are provisioned by an identity provider that issues unique, revocable credentials and reliably communicates credential revocation events to the dashcam/cloud system.

**Specifications (SPEC):**

- **SPEC1**: Encrypt all identifying images, video, and location histories at rest and in transit: use authenticated encryption (e.g., AES-256-GCM or equivalent) for stored data and TLS 1.2+ with strong ciphers for network transport. All long-term symmetric keys or key-encryption-keys must be generated and stored only in the device HSM or a cloud KMS; the software must never write plaintext keys to persistent storage or transmit them in the clear.
- **SPEC2**: Enforce authentication and authorization for any access to identifying data: require mutually authenticated sessions, RBAC with least privilege, and multi-factor authentication for investigator or privileged accounts. Deny access by default and log every access attempt with account ID, timestamp, target data ID, action, and result; sign or append these logs to an append-only tamper-evident store and retain them according to policy (e.g., X days).
- **SPEC3**: Apply data minimization and redaction by default: locally blur or redact faces, license plates, and precise geolocation in any data used for ML inference, previews, or transmission unless an explicit, logged, and authorized request is made. ML inference may run on minimized/derived representations; the software must not transmit raw, high-resolution identifying images or exact location coordinates to external services or users without the authorization workflow (MFA + justification) having completed and being recorded.
- **SPEC4**: Support cryptographic and credential lifecycle and incident response operations: implement key rotation (configurable cadence, e.g., 90 days), support remote revocation of device and user credentials, and enable remote wipe of locally stored identifying data on authenticated command. The software must generate alerts and create audit records for suspected compromise or successful revocation/wipe events and expose APIs for administrators to verify device wipe and credential status.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Relevant sightings are delayed, lost, or never reach authorized investigators, causing missed opportunities to recover the child, escalation of liability claims, and higher indemnity or reputational costs for insured parties.

**Requirement (REQ3):** Relevant sighting information that could materially affect search outcomes is delivered to authorized investigators while it remains actionable for search and recovery efforts.

**Assumptions (ASM):**

- **ASM1**: The dashcam device has access to a position sensor (GPS) at time of capture and the sensor provides location metadata with an accuracy of ±30 meters for ≥90% of captures in the operating area.
- **ASM2**: Network connectivity from the vehicle to backend services is intermittently available such that stored transmissions from the device are able to be delivered within 24 hours in normal operation (i.e., outages are transient and connectivity is restored within that window).
- **ASM3**: Authorized investigators maintain and monitor communication endpoints (authenticated accounts or devices) capable of receiving and reviewing incoming candidate-sighting notifications within 2 hours of delivery during active search periods.

**Specifications (SPEC):**

- **SPEC1**: For every candidate sighting produced (including ML-generated detections), the software shall record and persist: capture timestamp (UTC), GPS coordinates reported by the device, device identifier, the original image or video clip (or a verified lossless extract), ML model ID and version, ML-provided confidence score (numeric), and a label marking the record as a 'candidate sighting' (not a confirmation).
- **SPEC2**: The software shall assign a delivery priority and action path based on configurable rules that include ML confidence and sighting age. By default, if confidence ≥ 0.80 AND sighting age ≤ 4 hours, the system shall generate an immediate authenticated push notification to investigators; if confidence < 0.80 but ≥ 0.50 and age ≤ 24 hours, the system shall queue for batch review; otherwise the system shall mark the sighting low-priority for archival review. All thresholds must be configurable and logged when applied.
- **SPEC3**: When network delivery fails, the software shall store candidate sightings encrypted at rest and retry delivery using exponential backoff until either delivery succeeds or the sighting's time-to-live (TTL) of 24 hours from capture elapses. If TTL elapses without successful delivery, the software shall mark the sighting as 'undelivered—TTL expired' and record that state in the audit log; when connectivity is later available, undelivered items should not be auto-delivered without first applying the prioritization rules relative to current age.
- **SPEC4**: The software shall enforce authorization for receipt and viewing of candidate-sighting content: only authenticated investigator accounts with an active, case-linked authorization token may receive full images/videos. The system shall log delivery attempts, successful deliveries, investigator access (who viewed, when), and investigator review outcomes (e.g., 'verified', 'rejected', 'needs follow-up'), and shall expose these logs to authorized administrators for auditing.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Malicious or unauthorized actors submit spurious search requests or manipulate reports to create false incidents, leading to unnecessary investigations, resource costs, and an increase in fraudulent or nuisance claims that insurers must cover.

**Requirement (REQ4):** Search requests and any resulting sighting reports are initiated only for missing-child cases coordinated with recognized investigative authorities or designated partner organizations, and reported activities can be attributed to an accountable submitting party.

**Assumptions (ASM):**

- **ASM1**: Recognized investigative authorities and designated partner organizations issue digitally signed authorization tokens for each coordinated missing-child case; each token contains a case identifier, authorized submitter identifier, issuance timestamp, and expiration, and the authorities publish corresponding public keys or a verifiable key registry that the system can access.
- **ASM2**: Each submitting party (individual or organization) that may request searches is provisioned and recorded by the coordinating authority with a unique submitter identifier and contact metadata, and that identifier is either embedded in the authority-issued token or available in the authority's registry referenced by the token.
- **ASM3**: Authorities mark case status (active/closed/revoked) and publish revocation or expiration information for issued tokens (either in the token itself or via a registry) so that tokens for closed or revoked cases can be distinguished from tokens for active coordinated searches.

**Specifications (SPEC):**

- **SPEC1**: Accept a request to initiate a search only when the request includes an authority-issued authorization token; verify the token's digital signature against the authority's published public key, confirm required fields (case identifier, submitter identifier, issuance timestamp, expiration), and reject any request whose token fails signature verification, has missing required fields, or is expired.
- **SPEC2**: For every accepted search request and for every sighting report produced in relation to that request, record and persist: the full authorization token, the resolved submitter identifier and contact metadata, the verifying authority identifier, the verification timestamp, the verification outcome, and the software-generated report metadata (camera ID, location/time, ML confidence); store these records in an append-only, tamper-evident audit log that can be exported for external audit by insurers and investigators.
- **SPEC3**: Only transmit or surface candidate sighting alerts to investigators or partner recipients when the sighting is associated with a verified, active case token; label all ML-generated detections as 'candidate' (not confirmed), attach the associated token verification result and ML confidence, and prevent transmission of any detection that lacks an associated verified active token.
- **SPEC4**: Maintain and use a securely cached copy of authority public keys and revocation/expiry information to allow offline token verification within a defined freshness window; if verification cannot be completed (no cached valid key or token outside freshness window), queue the request/report and mark it pending verification without initiating external alerts or creating sighting transmissions until verification succeeds.

## 16. Device repair technicians and support staff

### Goals

- **G1**: Prevent exposure of identifying images or precise location information during repair and support activities.
- **G2**: Have access to sufficient diagnostic information to reproduce and resolve device faults without unnecessary access to sensitive user data.
- **G3**: Ensure devices remain operational or are restorable after legitimate repairs and firmware updates so technicians can complete service tasks.
- **G4**: Prevent unauthorized parties from gaining maintenance-level access through support interfaces or communication channels used for repairs.
- **G5**: Preserve the integrity and provenance of data relevant to active missing-child investigations and provide auditable records of support activity.

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Repair or support processes expose identifying images or precise location data from the dashcam to technicians, third parties, or bystanders, causing privacy breaches and potential legal liability for support staff.

**Requirement (REQ1):** Unauthorized parties do not gain access to identifying images or precise location information stored on devices or transmitted during repair or support activities.

**Assumptions (ASM):**

- **ASM1**: Technicians and support staff follow organizational repair policies that require explicit, verifiable owner consent before accessing or transmitting stored media or precise location data on a device.
- **ASM2**: Devices presented for repair remain in the state provided by the owner (e.g., locked with user credentials or encrypted) and owners either provide valid access credentials or explicitly state that credentials are not available.
- **ASM3**: Repair locations sometimes provide network connectivity to manufacturer or cloud support services, and when connected devices may attempt to sync diagnostic information or media unless network access is intentionally disabled.

**Specifications (SPEC):**

- **SPEC1**: Require authenticated technician identity (at least two-factor) and explicit owner authorization before the software allows any UI/API access to unredacted images or precise (sub-100m) GPS coordinates; record each access attempt with timestamp, actor identity, device identifier, and authorization token in an append-only audit log that cannot be modified by technician accounts.
- **SPEC2**: Provide a documented 'repair mode' that, by default, prevents access to identifying images and precise location by: (a) serving only redacted versions of images (on-device face/unique-feature masking) and (b) reducing reported location precision to coarse granularity (e.g., >=1 km). If on-device ML is used for redaction, the software must treat low-confidence redaction outcomes as redacted (fail-closed) and log the confidence score alongside the access record.
- **SPEC3**: For any remote support or firmware-update session, require mutual authentication (e.g., mTLS), present an explicit consent flow to the owner before sending any media or precise location, and limit default remote transmissions to non-identifying diagnostic indicators; when transmission of images or precise location is authorized, enforce end-to-end encryption and attach the consent record to the transmitted payload.
- **SPEC4**: Store identifying images and precise location metadata in an encrypted secure partition or keystore that is only decryptable with the owner's key or a time-limited escrow key released after verifiable owner authorization; attempts to mount or read that partition without proper authorization must return specific denial error codes and be recorded in the audit log.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Technicians are unable to diagnose or reproduce reported faults because necessary diagnostic information is unavailable or unusable, leading to prolonged outages and increased support effort.

**Requirement (REQ2):** Technicians can access sufficient non-identifying diagnostic information to reproduce and resolve reported device faults without accessing identifying images or precise location data.

**Assumptions (ASM):**

- **ASM1**: Devices and their onboard firmware produce and locally retain timestamped diagnostic telemetry when faults occur, including error codes, system resource metrics, sensor status, and low-resolution motion/scene summaries, for at least 14 days after the event.
- **ASM2**: Network connectivity between devices and the backend is intermittently available such that devices can successfully upload stored diagnostic telemetry to the backend within 72 hours of capture when connectivity is present.
- **ASM3**: Applicable privacy policy, user consent, and legal constraints permit sharing non-identifying diagnostic metadata (excluding raw identifiable images and sub‑meter GPS coordinates) with authorized repair technicians for the purpose of diagnosis and repair.

**Specifications (SPEC):**

- **SPEC1**: Provide an authenticated, role-restricted diagnostics interface for technicians that returns only non-identifying diagnostic data: timestamped error codes, system resource metrics, sensor health/status, ML model version and output labels with confidence scores, and visual summaries that are provably non-reconstructable (e.g., fixed-size 32x32 blurred thumbnails or one-way feature embeddings with no stored inverse mapping). The interface must not return raw image pixels or GPS coordinates finer than 1 km resolution. Responses must include device-local timestamps and be retained/available for at least 14 days.
- **SPEC2**: When exporting diagnostics for a reported fault, include synchronized sequence identifiers and monotonic timestamps for all relevant sensor streams and events (e.g., imu, motion state, audio events, model inferences) in a documented machine-readable schema (JSON/NDJSON). Exports must omit raw pixel data and precise GPS while providing relative motion traces and coarse location bins (<=1 km). Exports must be verifiable by automated tests that confirm (a) absence of raw images, (b) timestamp continuity, and (c) location precision limits.
- **SPEC3**: Record an auditable access trail for all technician diagnostic accesses and exports: log user identity, role, requested device identifier (hash or truncated id that does not reveal full device serial), timestamp, and export contents metadata. Store audit logs for at least 90 days and provide an API to query and verify audit entries for compliance testing.
- **SPEC4**: Provide a diagnostics replay sandbox/tooling that can ingest exported non-identifying telemetry (sensor streams, model input embeddings, model version identifiers, and timestamps) and reproduce the sequence of events to assist root-cause analysis. The tooling must surface model version and confidence scores, and tests must verify that known fault signatures present in device telemetry are reproducible in the sandbox using only the exported non-identifying data.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Legitimate firmware updates or repair procedures render devices inoperable or degrade core recording/search functionality, causing downtime, additional repairs, or replacement costs for technicians and customers.

**Requirement (REQ3):** After legitimate repair or update procedures, devices are either operational for their core recording and search functions or can be restored to operational condition by technicians within 72 hours.

**Assumptions (ASM):**

- **ASM1**: A qualified technician or authorized support staff will have physical access to the device within 72 hours and will have any required authorized recovery media or tools (e.g., USB recovery image, technician console, or hardware adapter) available at the repair location.
- **ASM2**: The device can be connected to a stable power source (mains or charged battery) during repair or update attempts so that power loss will not interrupt recovery procedures.
- **ASM3**: If hardware replacement is required to restore core recording or search functions, replacement parts (e.g., storage modules, connectors) are available from local repair inventory or vendor within the 72-hour restoration window.

**Specifications (SPEC):**

- **SPEC1**: The software must perform firmware and model updates atomically: verify cryptographic signatures and integrity of update packages before applying; stage the update in a separate partition; if the device fails to boot into the new firmware or complete a post-update self-check within 5 minutes, automatically revert to the previously running verified firmware and boot into an operational state.
- **SPEC2**: Before applying any update or performing any repair-affecting operation, the software must create and protect a backup of core recording files, search indices, and configuration metadata in a non-overwritable storage area; provide a logged, verifiable restore operation that a technician can invoke to recover these artifacts without data loss.
- **SPEC3**: The software must expose a technician-accessible recovery mode (activatable via physical interface or authenticated local connection) that accepts signed recovery images over USB or local Ethernet, provides a downloadable diagnostic bundle (including boot logs, firmware and model versions, storage health metrics, and error codes), and implements scripted restore/reflash operations that complete on-device within 2 hours under normal power.
- **SPEC4**: For ML components affecting search functionality, the software must record model version metadata and run an automated post-update model health test using an embedded test dataset and predefined performance thresholds; if the updated model fails to meet thresholds, the software must rollback to the previous model and enable a documented fallback search mode (e.g., metadata-based search) to maintain core search capability until a technician restores or replaces the model.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Unauthorized remote parties exploit maintenance interfaces or common repair communication channels (e.g., local wireless or wired connections used in support) to obtain maintenance-level access, allowing data exfiltration or malicious modification that implicates technicians.

**Requirement (REQ4):** Maintenance interfaces and repair communication channels are not accessible to unauthorized parties; maintenance-level access is only possible by authorized personnel.

**Assumptions (ASM):**

- **ASM1**: Authorized maintenance personnel possess and can present manufacturer-issued, unique cryptographic credentials (for example, client X.509 certificates or one-time HMAC tokens) during repair sessions; the device can observe and verify those credentials.
- **ASM2**: Remote repair sessions, when used, are initiated via vendor-controlled support channels that are identifiable to the device (for example, by a known certificate chain, server identity, or session ID) rather than by arbitrary, unidentifiable public intermediaries.
- **ASM3**: Local physical maintenance access (e.g., USB, serial, or Bluetooth pairing) is performed only when an authorized person is physically present and the device can observe a local consent indicator (for example, a maintenance-mode hardware button press, secure proximity token, or other verifiable local input).

**Specifications (SPEC):**

- **SPEC1**: The software must keep all maintenance-level interfaces disabled by default and enable them only after successful cryptographic mutual authentication: verify a presented client credential (e.g., client X.509 certificate or one-time token), validate the certificate chain and revocation status, and permit maintenance mode only if verification succeeds; failed verifications must leave maintenance interfaces disabled and be recorded in the audit log.
- **SPEC2**: All maintenance commands and tool interactions must be accepted only over authenticated, integrity-protected channels and only if each command or update is accompanied by a valid digital signature from an authorized maintenance key; the software must validate signatures and signed command manifests before executing any maintenance-level operation and reject and log unsigned or invalidly signed inputs.
- **SPEC3**: For remotely initiated maintenance sessions, the software must require a verifiable local consent action (for example, a hardware maintenance confirmation button press or presence of a local secure token) within a bounded time window (e.g., 60 seconds) before enabling maintenance-level access; if local consent is not observed within the window, the session must be denied and logged.
- **SPEC4**: The software must produce an append-only, tamper-evident audit log for all maintenance access attempts and actions (including authenticated principal identity, timestamp, session identifier, and cryptographic verification results); the log entries must be cryptographically signed. The software must run an anomaly-detection component to flag unusual maintenance-access patterns (for example, repeated failed authentications, attempts from unexpected device state, or unexpected sequence of commands) and, when a session is flagged, require explicit out-of-band human authorization before permitting maintenance-level operations to proceed.

#### H5 / REQ5

**Related Goal:** G5

**Loss:** Support staff inadvertently modify, delete, or fail to preserve images or logs relevant to active missing-child investigations, undermining investigations and exposing technicians and organizations to legal or reputational harm.

**Requirement (REQ5):** Data and logs related to active missing-child investigations are preserved, and any access, modification, or deletion of those items is recorded and attributable so unintended changes are detectable.

**Assumptions (ASM):**

- **ASM1**: Devices and individual media items that are part of active missing-child investigations are recorded in a case-management or asset-tracking system with an accessible status flag (e.g., 'active_investigation') that the dashcam software can query via API.
- **ASM2**: Device and server clocks (timestamps) are synchronized to an authoritative time source (e.g., NTP) within a bounded skew (e.g., ≤5 seconds) so events and logs from different systems can be reliably correlated and attributed by the software.
- **ASM3**: Repair and support activities (file reads, writes, mounts, hardware connections) generate observable system-level events or metadata (e.g., filesystem change events, kernel audit logs, USB/hardware connection logs) that the dashcam software or local agent can read to detect technician actions while the device is in repair custody.

**Specifications (SPEC):**

- **SPEC1**: On intake of any device or media flagged as part of an active missing-child investigation, the software must automatically create a forensically sound, bit-for-bit copy (immutable image) of all images and relevant logs and store that copy in tamper-evident storage (cryptographic hashes recorded). The original media must be mounted read-only or otherwise write-protected until explicit, logged, authorized override is performed. The system must periodically (configurable, e.g., daily) re-verify stored-image integrity by checking stored hashes.
- **SPEC2**: All accesses, modifications, attempted deletions, and successful deletions of items tied to active investigations must be recorded in an append-only audit log that includes: timestamp, authenticated user account ID, user role, device/media ID, action type, source IP or terminal identifier, and any provided justification. Audit entries must be cryptographically signed or stored with tamper-evidence and replicated to at least one remote, write-once location within a bounded time window (e.g., 10 minutes).
- **SPEC3**: The software must enforce role-based access control for repair/support staff: by default, support accounts may not modify or delete preserved investigation items. Any requested write/delete operation on preserved items must require a documented two-person authorization (two distinct authenticated approvers), produce a required justification field, be denied if approval is absent, and generate an immediate alert to designated investigators. The system must provide APIs and UI controls to lock/unlock items and to produce attestable logs of the authorization workflow.

## 17. Malicious actors (abusers, stalkers, hackers)

### Goals

- **G1**: Obtain identifying images, location metadata, or recorded footage of chosen targets for surveillance or exploitation.
- **G2**: Remain anonymous and avoid attribution while interacting with the dashcam system or its partners.
- **G3**: Inject, manipulate, or submit false sightings or tampered footage to misdirect searches, create false leads, or falsely implicate others.
- **G4**: Disrupt, degrade, or evade coordinated search operations (e.g., by causing denial-of-service, flooding with spurious data, or blocking legitimate communications).

### Losses, Requirements, Assumptions, and Specifications

#### H1 / REQ1

**Related Goal:** G1

**Loss:** Unauthorized parties obtain identifying images or location information from dashcam recordings or search results and use them to stalk, harass, or locate individuals.

**Requirement (REQ1):** Identifying images, location metadata, and other footage that can be used to track or locate recorded individuals are not accessible to unauthorized parties.

**Assumptions (ASM):**

- **ASM1**: Physical custody of dashcam devices and removable storage is maintained by authorized owners or custodians and unauthorized individuals do not obtain persistent physical access to the device or removable storage media.
- **ASM2**: An authoritative, externally maintained registry of authorized investigator accounts and active case identifiers exists and is available for the software to query to verify whether a requester is permitted access to identifying footage or location data.
- **ASM3**: Requesters who are legitimately authorized (e.g., investigators) will present required legal or organizational credentials through the registered channels described in the authoritative registry, and external identity/credential providers will be able to validate those credentials.

**Specifications (SPEC):**

- **SPEC1**: Encrypt all recorded footage and associated metadata at rest on the device and in backend storage using per-device or per-record keys; decryption keys must be stored and used only within a protected key management system (e.g., HSM or equivalent) and the software must deny access to decrypted content unless the requester is authenticated and explicitly authorized for that case.
- **SPEC2**: Strip or redact precise location metadata (GPS coordinates) and exact timestamps from any images, thumbnails, or video clips delivered to accounts that are not confirmed, case-authorized investigators; when delivering low-privilege search results provide only low-resolution thumbnails with no EXIF or machine-readable location fields and with visible watermarks or obfuscation to prevent reuse for tracking.
- **SPEC3**: Enforce fine-grained access control for all queries and downloads: require strong authentication (including multi-factor authentication) and an explicit per-case authorization check against the external registry before returning identifying images or precise location data; record immutable audit logs of all access attempts and notify administrators on anomalous patterns (e.g., bulk exports, repeated failed authorizations, access from new geolocations) and automatically throttle or suspend suspicious accounts pending review.
- **SPEC4**: When ML components produce candidate sightings or matches, label outputs as 'candidate' and ensure that any automatically-shared or user-viewable media for non-authorized users is sanitized (e.g., faces blurred, license plates obfuscated) regardless of model confidence; retain and only release full-resolution, unsanitized originals through an audited, authorized workflow that requires the checks in SPEC1 and SPEC3.

#### H2 / REQ2

**Related Goal:** G2

**Loss:** Malicious actors are able to masquerade as investigators, partners, or device owners to receive sensitive search results or access capabilities reserved for authorized entities.

**Requirement (REQ2):** Only authorized investigators and verified partner organizations receive confirmed sightings or identifying information; requests from unverified third parties are not treated as authorized.

**Assumptions (ASM):**

- **ASM1**: Authorized investigators and verified partner organizations possess unique, verifiable cryptographic credentials (e.g., X.509 certificates, signed tokens, or organization-issued API keys) that can be validated by the system against a reachable verification service or certificate authority.
- **ASM2**: An authoritative partner registry and credential-revocation mechanism (e.g., OCSP, CRL, or a trusted API) exists and is updated by the verifying authority; the registry and revocation information are reachable by the system with sufficient frequency to reflect changes in authorization status within a defined window (e.g., hours).
- **ASM3**: Authorized investigators and partner organizations exercise operational control over their credentials and registered devices (e.g., do not intentionally share private keys or account passwords with unverified third parties) and report suspected compromise to the verifying authority within a bounded time.

**Specifications (SPEC):**

- **SPEC1**: Deny access to confirmed sightings or any identifying information unless the requester successfully authenticates and is authorized: validate cryptographic credentials (mutual TLS or signed tokens) against the authoritative partner registry and check that the requester’s credential status is not revoked before fulfilling the request.
- **SPEC2**: Require multi-factor authentication and device binding for investigator accounts; for any ML-flagged confirmed sighting that includes identifying information, require a human reviewer with authorized investigator credentials to positively confirm the sighting in the system UI before releasing identifying details, except when an explicit documented emergency override is invoked (override must produce an auditable justification and require elevated authentication).
- **SPEC3**: Periodically fetch and cache the authoritative partner registry and revocation data; reject or throttle access when the registry cannot be reached for more than a configured time window, and immediately deny requests for credentials marked revoked in the latest fetched data.
- **SPEC4**: Log every request for sightings and every delivery of identifying information with requester identity, credential used, request source (IP/device id), timestamp, and sighting id; run anomaly-detection rules (or an auditable ML model) on access patterns and automatically block or escalate requests that match high-risk patterns (e.g., credential reuse from new devices, rapid enumeration); require manual administrator review before unblocking.

#### H3 / REQ3

**Related Goal:** G3

**Loss:** Manipulated or false submissions from malicious actors cause investigators to pursue incorrect leads, expose innocent people, or divert resources from legitimate searches.

**Requirement (REQ3):** Automated model outputs and unverified user submissions are not treated as confirmed sightings on their own; investigative actions require corroboration or verification before being escalated to field response.

**Assumptions (ASM):**

- **ASM1**: Authorized investigators or designated reviewers will inspect received candidate sightings within a defined response window (e.g., within 72 hours) such that human verification can reasonably occur before escalation.
- **ASM2**: At least some genuine corroborating evidence sources (e.g., other dashcam submissions, public or private CCTV feeds, police records, or eyewitness reports) exist and are accessible for the geographic area of a reported sighting when corroboration is possible.
- **ASM3**: A subset of submitted media includes device-generated metadata (timestamp, GPS, device ID) that are preserved through transmission and available to the software for analysis; when such metadata are absent or truncated this condition is observable by the system (e.g., missing fields or checksum failures).

**Specifications (SPEC):**

- **SPEC1**: The software must label every automated detection and every user-submitted sighting as 'candidate' or 'unverified' in the UI and internal state; the software must not create or schedule any field response ticket automatically based solely on an automated detection or a single unverified user submission.
- **SPEC2**: The software must enforce escalation rules requiring either (A) at least two independent corroborating evidences (different device IDs, different camera systems, or an independent eyewitness report) that reference the same time and location window, or (B) an explicit manual verification action by an authorized investigator recorded in the system, before generating a field response.
- **SPEC3**: For every candidate sighting the software must display and immutably log provenance and metadata: uploader identity (account ID), device ID (if present), upload timestamp, media file hash, GPS coordinates (if present), and model confidence score; the software must automatically flag sightings with missing or inconsistent metadata as 'requires verification' and prevent automatic escalation for those sightings.
- **SPEC4**: The software must compute and maintain a trust score for submitters based on verifications in historical submissions; it must apply stricter handling for low-trust or new accounts (rate-limit, deprioritize in investigator queues, and block auto-escalation); any override allowing escalation from a low-trust submitter must require an explicit investigator confirmation action that is logged.

#### H4 / REQ4

**Related Goal:** G4

**Loss:** Coordinated searches are delayed or degraded because malicious actors cause device unavailability, flood the system with spurious data, or otherwise interfere with communications and processing.

**Requirement (REQ4):** Search coordination and delivery of relevant sightings to authorized investigators remain resilient to individual device failures and to attempts to overwhelm or interfere with the system, so authorized parties receive relevant sightings within an acceptable time window despite isolated interference.

**Assumptions (ASM):**

- **ASM1**: For each active search region, at least one uncompromised device (distinct device ID) within the region can transmit at least one candidate sighting to the backend within the system-configured maximum tolerable transmission delay (e.g., the configured delivery window) despite intermittent local outages.
- **ASM2**: Cryptographic credentials and primitives used for device and investigator authentication are not broken by attackers (i.e., attackers cannot forge valid signatures for device IDs or investigator accounts within the timeframe that would affect a search).
- **ASM3**: When a genuine sighting occurs, at least one independent, uncompromised device in the vicinity will generate observable sensor data (image and timestamped location metadata) whose sensor-reported timestamp and geolocation fall within the device's stated accuracy bounds and can be correlated by the software to the real-world event.

**Specifications (SPEC):**

- **SPEC1**: Require cryptographic authentication: the system must accept only device reports and investigator queries that present valid signatures from registered keys; reject and log messages with invalid signatures; maintain a revocation list that propagates to all ingestion endpoints within the configured TTL (e.g., 5 minutes) and causes rejected messages from revoked IDs.
- **SPEC2**: Ingestion hardening and throttling: enforce per-device and per-region ingestion limits (e.g., max 10 candidate-sighting submissions per device per minute and configurable regional backpressure thresholds) and enforce exponential backoff for exceeding devices; when global or regional ingestion exceeds configured capacity, prioritize delivery of sightings by priority score (see SPEC4), enqueue lower-priority items to durable storage and surface overload metrics and alerts to operators.
- **SPEC3**: Durability and replication: persist every accepted candidate sighting to a durable, append-only queue and replicate each persisted sighting to at least three geographically-separated processing nodes before acknowledging the device; provide guaranteed-at-least-once delivery to downstream search/coordinator services and expose delivery and replication status via monitoring APIs.
- **SPEC4**: Corroboration, ML scoring, and anomaly quarantine: assign each candidate sighting an ML-derived confidence score and calibrated uncertainty; never mark ML detections as confirmed—present them as candidate sightings with score and provenance. Automatically escalate and deliver sightings immediately to investigators when at least two independent devices (distinct device IDs not sharing the same owner/vehicle registration) report candidate sightings within 500 meters and within 15 minutes. Run automated anomaly detection on reporting patterns (e.g., per-device burstiness, identical images across many devices, synchronized timestamps) and temporarily quarantine devices that exceed suspicious-behavior thresholds while continuing to accept and prioritize corroborated reports from other devices; log quarantines for operator review.
