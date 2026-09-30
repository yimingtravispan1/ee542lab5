# EE542 Lab 5 Report: Mobile Phone IoT Network

## Objective

Build an end-to-end IoT system that sends location data from mobile phones running OwnTracks to a ThingsBoard Community Edition server on an AWS EC2 instance. Display live telemetry on a map and develop a custom mapping solution using data from multiple phones.

## System Setup

- **Cloud server:** [EC2 instance type, Ubuntu version, public IP or hostname]
- **Software:** OpenJDK 17, PostgreSQL 16, ThingsBoard Community Edition, OwnTracks
- **ThingsBoard database:** PostgreSQL database named `thingsboard`
- **Queue:** Default in-memory queue
- **Devices:** [Phone/device names and number of phones]
- **Data flow:** OwnTracks on each phone → HTTP telemetry endpoint → ThingsBoard device → dashboard and custom map

**Setup procedure:** Install the software, configure ThingsBoard to use PostgreSQL, run its installation script with demo data, and start the service. Create a ThingsBoard device for each phone and configure OwnTracks to send HTTP messages to its device endpoint. Record completion and any issues here: [Setup notes]. Omit device tokens and database passwords.

**Setup evidence:** [Insert screenshots or a short description of the EC2 instance, running service, device list, and OwnTracks configuration. Hide credentials and tokens.]

## Telemetry Verification and Dashboard

**Verification procedure:** Check each device's **Latest Telemetry** tab for incoming values. Configure a ThingsBoard dashboard with an OpenStreetMap widget using `lat` for latitude and `lon` for longitude. Record the observed results below.

| Device | Telemetry received? | `lat`/`lon` updating? | Map position updates? |
| --- | --- | --- | --- |
| [Phone 1] | [Result] | [Result] | [Result] |
| [Phone 2] | [Result] | [Result] | [Result] |
| [Additional phones] | [Result] | [Result] | [Result] |

**Evidence:** [Insert a Latest Telemetry screenshot and a dashboard screenshot showing the phone positions.]

## Custom Mapping Solution

**Application idea:** We implemented a **Team Meet-Up Tracker** that shows multiple phones on the same real-time map and indicates each phone's status relative to a predefined meetup point.

**Inputs:** GPS telemetry from multiple phones, including `lat` and `lon`, plus a derived `meetupStatus` value for each phone.

**Implementation:** All phone devices and a fixed `Meetup-Point` were added to the same ThingsBoard OpenStreetMap widget. Phone locations update in real time from OwnTracks telemetry. A calculated `meetupStatus` is used to indicate whether a phone is far from, approaching, near, or at the meetup point. The map label displays the device name and current status, and the label color changes according to the status.

**Design decisions:** The solution keeps all devices on one map so the team can quickly compare locations. Status labels were added to make the meetup state easy to understand without opening separate widgets.

**Observed result:** During testing, phone markers updated as new GPS data arrived, and the displayed meetup status changed as devices moved relative to the meetup point.

**Evidence:** [Insert screenshot of the completed Team Meet-Up Tracker showing multiple phones, the Meetup-Point, and status labels.]