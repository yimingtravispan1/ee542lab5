# EE542 Lab 5 Report: Mobile Phone IoT Network

## Custom App Objective

Build an end-to-end IoT system that sends location data from mobile phones running OwnTracks to a ThingsBoard Community Edition server on an AWS EC2 instance. Display live telemetry on a map and develop a custom mapping solution using data from multiple phones.

## Individual Setup Contribution

The cloud-side environment and the initial end-to-end phone test were completed before the multi-phone integration stage.

The setup work included:

- Creating the AWS networking environment and launching an Ubuntu EC2 instance.
- Installing OpenJDK 17, PostgreSQL 16, and ThingsBoard Community Edition.
- Creating the PostgreSQL database used by ThingsBoard and verifying that the ThingsBoard service was running correctly.
- Creating the initial ThingsBoard device, `JYU-Phone`.
- Configuring Android OwnTracks to send HTTP telemetry to ThingsBoard.
- Verifying OwnTracks telemetry fields including `lat`, `lon`, `acc`, `alt`, and `batt`.
- Creating an OpenStreetMap dashboard and confirming that the phone location could be displayed using the `lat` and `lon` telemetry keys.

### Android OwnTracks Compatibility Issue

During Android testing, OwnTracks repeatedly retried messages because it could not correctly handle the empty HTTP response body returned after a successful ThingsBoard telemetry POST.

To solve this issue, a lightweight HTTP proxy was added on the EC2 instance. The proxy forwards the telemetry payload to ThingsBoard and returns a valid empty JSON array (`[]`) to OwnTracks.

After this adjustment, the retry queue was cleared and location telemetry could be uploaded normally.

### Team Handoff

After the single-phone pipeline was verified, the cloud environment was ready for the rest of the team.

Each team member only needs to:

1. Create a separate ThingsBoard device.
2. Use the corresponding device token in OwnTracks.
3. Verify that `lat` and `lon` appear in **Latest Telemetry**.
4. Add the device to the shared map dashboard.

The PostgreSQL password and SSH private key are not required for normal phone-side testing or dashboard configuration.

## Telemetry Verification and Dashboard

### Verification Procedure

1. Check each device's **Latest Telemetry** tab for incoming values.
2. Configure a ThingsBoard dashboard with an OpenStreetMap widget using `lat` for latitude and `lon` for longitude.
3. Record the observed results below.

### Verification Results

| Device | Telemetry received? | `lat`/`lon` updating? | Map position updates? |
| --- | --- | --- | --- |
| `JYU-Phone` | Yes | Yes | Yes |
| `YuXia-Phone` | Yes | Yes | Yes |
| `Yiming-Phone` | Yes | Yes | Yes |

## Custom Mapping Solution

### Application Idea

We implemented a **Team Meet-Up Tracker** that shows multiple phones on the same real-time map and indicates each phone's status relative to a predefined meetup point.

### Inputs

GPS telemetry from multiple phones, including `lat` and `lon`, plus a derived `meetupStatus` value for each phone.

### Implementation

All phone devices and a fixed `Meetup-Point` were added to the same ThingsBoard OpenStreetMap widget. Phone locations update in real time from OwnTracks telemetry.

A calculated `meetupStatus` is used to indicate whether a phone is far from, approaching, near, or at the meetup point. The map label displays the device name and current status, and the label color changes according to the status.

### Design Decisions

The solution keeps all devices on one map so the team can quickly compare locations. Status labels were added to make the meetup state easy to understand without opening separate widgets.

### Observed Result

During testing, phone markers updated as new GPS data arrived, and the displayed meetup status changed as devices moved relative to the meetup point.
