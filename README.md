# EE542 Lab 5: Mobile Phone IoT Network

This project connects mobile phones running OwnTracks to a ThingsBoard Community Edition server on AWS EC2. The **Team Meet-Up Tracker** described in the report displays multiple phones on an OpenStreetMap dashboard and shows their status relative to a meetup point.

## Repository Contents

| File | Description |
| --- | --- |
| [report.md](report.md) | Setup contribution, telemetry verification results, application design, and observed behavior. |
| [proxy/owntracks_proxy.py](proxy/owntracks_proxy.py) | HTTP compatibility proxy for Android OwnTracks and ThingsBoard. |

The dashboard and meetup-status configuration are described in the report; their configuration exports and calculation code are not included in this repository.

## System Overview

Phones send HTTP telemetry to their ThingsBoard devices. Android phones that encounter the response-parsing issue described in the report can send through the compatibility proxy:

```text
OwnTracks → HTTP proxy (:8081) → ThingsBoard (:8080) → PostgreSQL
                                      ↓
                             OpenStreetMap dashboard
```

The report records successful telemetry and map updates for `JYU-Phone`, `YuXia-Phone`, and `Yiming-Phone`. Location fields are `lat` and `lon`; other reported telemetry includes `acc`, `alt`, and `batt`.

## Environment

- An Ubuntu EC2 instance running ThingsBoard Community Edition.
- OpenJDK 17 and PostgreSQL 16, with a database named `thingsboard`.
- OwnTracks on each participating phone.
- Python 3 for the compatibility proxy. The script uses only the Python standard library.

## Phone and Dashboard Setup

1. Create a separate ThingsBoard device for each phone and obtain its device token.
2. Configure OwnTracks to send HTTP telemetry to that device's endpoint:

   ```text
   http://<EC2_HOST>:8080/api/v1/<DEVICE_TOKEN>/telemetry
   ```

3. Check the device's **Latest Telemetry** tab for incoming values and updating `lat` and `lon` fields.
4. Add the phone devices to a ThingsBoard OpenStreetMap widget. Set the latitude key to `lat` and the longitude key to `lon`.
5. For the Team Meet-Up Tracker, configure a fixed `Meetup-Point` and the derived `meetupStatus` described in [the report](report.md#custom-mapping-solution).

## Android HTTP Compatibility Proxy

The proxy forwards each POST body to ThingsBoard and returns HTTP 200 with an empty JSON array (`[]`) after a successful upstream request. On an upstream exception, it returns HTTP 500. This addresses the OwnTracks retry behavior documented in the report.

### Run the Proxy

1. On the EC2 instance, edit `THINGSBOARD_URL` in `proxy/owntracks_proxy.py` to use the intended ThingsBoard device token:

   ```python
   THINGSBOARD_URL = "http://127.0.0.1:8080/api/v1/<DEVICE_TOKEN>/telemetry"
   ```

2. From the repository root, start the proxy:

   ```bash
   python3 proxy/owntracks_proxy.py
   ```

3. Ensure the EC2 network configuration allows the phone to reach TCP port `8081`, then configure the phone's OwnTracks HTTP URL as:

   ```text
   http://<EC2_HOST>:8081/
   ```

4. Verify incoming telemetry in ThingsBoard. Use `Ctrl+C` to stop the foreground proxy process.

### Multiple Phones

The current proxy forwards every request to one fixed ThingsBoard device token; it does not route requests by incoming URL or phone identity. Phones sharing this proxy instance therefore send data to the same device.

For separate devices, use each phone's direct ThingsBoard endpoint where compatible. If multiple phones require the proxy, run separate copies configured with distinct device tokens and listening ports, or extend the proxy to support per-device routing. Separate copies require changing the port in the final `HTTPServer` call as well as `THINGSBOARD_URL`.
