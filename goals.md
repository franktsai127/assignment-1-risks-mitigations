# Goals and Measurement

## 1. Organizational Goals

The dashcam company has several organizational goals for the missing-child search feature:

1. Differentiate its dashcam products from competitors by offering a socially valuable AI-enabled feature.
2. Increase customer interest and product adoption by providing functionality beyond traditional video recording.
3. Build a positive reputation by supporting public safety and child protection efforts.
4. Develop reusable AI and edge-computing capabilities that may support future product features.
5. Maintain customer trust by protecting privacy and avoiding unexpected data usage or costs.
6. Reduce legal, regulatory, and reputational risks associated with person recognition technology.

## 2. System Goals

The system should support the search for missing children using dashcam recordings.

1. Detect possible appearances of a missing child in recorded dashcam footage.
2. Report useful sightings to authorized organizations quickly enough to support an active search.
3. Minimize missed relevant sightings.
4. Minimize incorrect reports that could waste investigators' time or create harm.
5. Protect the privacy of dashcam users and people appearing in recorded footage.
6. Operate under the connectivity, power, storage, and processing limitations of different dashcam models.
7. Restrict searches and access to authorized missing-child cases.
8. Keep data usage and processing costs reasonable for users.

## 3. User Goals

### 3.1 Law Enforcement and Search Authorities

Law enforcement and other authorized search organizations want to:

1. Receive relevant and timely information about possible sightings.
2. Avoid spending excessive time investigating incorrect matches.
3. Understand where and when a possible sighting occurred.
4. Receive information that can be verified using supporting footage or metadata.

### 3.2 Families of Missing Children

Families want to:

1. Increase the chance that the missing child is located safely.
2. Receive useful information as quickly as possible.
3. Avoid delays caused by missed sightings.
4. Avoid harmful confusion caused by large numbers of incorrect reports.

### 3.3 Dashcam Owners

Dashcam owners want to:

1. Contribute to missing-child searches with minimal effort.
2. Maintain control over how their recordings and devices are used.
3. Avoid excessive mobile data, battery, storage, or processing costs.
4. Protect their privacy and the privacy of people captured in their recordings.
5. Continue using normal dashcam functionality without significant performance degradation.

### 3.4 People Recorded by Dashcams

People appearing in dashcam footage want to:

1. Avoid unnecessary identification or tracking.
2. Prevent their images from being retained or shared beyond the intended search purpose.
3. Reduce the chance of being incorrectly identified as a missing child.
4. Have their personal information protected from unauthorized access.

### 3.5 Non-Profit Child Safety Organization

The partner non-profit organization wants to:

1. Improve the effectiveness of missing-child searches.
2. Coordinate searches with authorities efficiently.
3. Ensure the system is used only for legitimate child-safety purposes.
4. Maintain public trust in the organization and the search process.

## 4. Model Goals

The person recognition model should:

1. Correctly identify images or video frames that may contain the missing child.
2. Maintain a low false-negative rate so that useful sightings are not missed.
3. Maintain a sufficiently low false-positive rate so that investigators are not overwhelmed by incorrect matches.
4. Perform reliably under difficult conditions such as low light, motion blur, partial occlusion, and unusual camera angles.
5. Produce results quickly enough to support timely reporting.
6. Operate within the computational constraints required by the selected deployment architecture.

## 5. Relationships Between Goals

The goals at different levels influence each other.

Higher recognition accuracy supports the system goal of identifying useful sightings. In particular, reducing false negatives increases the probability that relevant footage is detected, while reducing false positives decreases unnecessary work for authorities.

Timely model inference and system processing support the goal of quickly reporting possible sightings. This benefits law enforcement, child-safety organizations, and families because recent location information is generally more useful during a search.

Privacy protections support dashcam-owner and bystander goals while also supporting the company's organizational goal of maintaining customer trust and reducing legal and reputational risk.

Efficient use of computation, battery, network bandwidth, and storage supports dashcam-owner goals and makes the feature practical across different dashcam models.

The organizational goal of creating a competitive product depends on the system being useful, trustworthy, safe, and practical. Poor model quality, excessive false reports, privacy violations, or high user costs could reduce customer trust even if the feature provides some useful sightings.

## 6. Measurements

### 6.1 Organizational Goal Measurement

**Goal:** Increase customer interest in the company's dashcams through the missing-child search feature.

**Measure:**  
The percentage of prospective or new customers who report that the missing-child search feature positively influenced their purchase decision.

**Data:**  
A short post-purchase survey provided to customers who purchase a supported dashcam. The survey asks whether the feature had no influence, minor influence, moderate influence, or major influence on their decision.

**Operationalization:**  
Collect survey responses for three months after the feature launches. Count responses of "moderate influence" or "major influence" as positive. Divide the number of positive responses by the total number of valid responses. Report the percentage monthly and compare it with a predefined product target.

### 6.2 System Goal Measurement

**Goal:** Report useful possible sightings to authorities quickly.

**Measure:**  
End-to-end sighting reporting latency.

**Data:**  
System logs containing the timestamp when relevant dashcam footage becomes available for analysis and the timestamp when the resulting sighting report becomes available to the authorized search organization.

**Operationalization:**  
For every generated sighting report, calculate the difference between the two timestamps. Report the median and 95th percentile latency. The system team can define an acceptable threshold and measure the percentage of reports delivered within that threshold.

### 6.3 User Goal Measurement

**Stakeholder:** Law enforcement and authorized search personnel.

**Goal:** Avoid wasting investigation time on incorrect sightings.

**Measure:**  
The proportion of system-generated sighting reports that investigators determine to be useful enough for further investigation.

**Data:**  
For each sighting report reviewed by authorized personnel, record whether the report is classified as useful for follow-up or dismissed as an incorrect or irrelevant match.

**Operationalization:**  
During active searches, collect the review outcome for every system-generated report. Divide the number of reports marked useful for follow-up by the total number of reviewed reports. Track the rate across searches and deployment conditions.

### 6.4 Model Goal Measurement

**Goal:** Minimize missed appearances of a missing child.

**Measure:**  
Recall of the person recognition model on representative dashcam footage.

**Data:**  
A labeled evaluation dataset containing dashcam images and video frames in which the target person is known to be present or absent. The dataset should include realistic conditions such as low light, motion blur, partial occlusion, and different camera angles.

**Operationalization:**  
Run the model on the fixed evaluation dataset using the planned production decision threshold. Count true positives and false negatives and calculate:

Recall = True Positives / (True Positives + False Negatives)

Report overall recall and recall for important environmental slices such as low-light footage, motion blur, and partial occlusion.