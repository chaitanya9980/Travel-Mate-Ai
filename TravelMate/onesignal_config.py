"""
OneSignal Configuration for TravelMate AI
Handles push notifications to users
"""

import requests
import json

# OneSignal configuration - Replace with your actual credentials
ONESIGNAL_CONFIG = {
    'app_id': '3e01ba39-b68f-4f2f-bdd3-5f5c1182d1a8',
    'api_key': 'os_v2_app_hya3uonwr5hs7potl5obdawrvb2ddby7pyluhfnelpix65pibxvf2upfkxaozsauzoz7zntfu7vnhnnlunpephzomw6dstjbkb6uy4i',
    'rest_api_key': 'YOUR_ONESIGNAL_REST_API_KEY'
}

_PLACEHOLDERS = {
    'YOUR_ONESIGNAL_APP_ID',
    'YOUR_ONESIGNAL_API_KEY',
    'YOUR_ONESIGNAL_REST_API_KEY'
}

def _is_placeholder(value):
    return not value or value in _PLACEHOLDERS

def _resolve_auth_key():
    rest_api_key = ONESIGNAL_CONFIG.get('rest_api_key')
    api_key = ONESIGNAL_CONFIG.get('api_key')
    if not _is_placeholder(rest_api_key):
        return rest_api_key
    if not _is_placeholder(api_key):
        return api_key
    return None

_AUTH_KEY = _resolve_auth_key()

# Check if OneSignal is configured
ONESIGNAL_ENABLED = (
    not _is_placeholder(ONESIGNAL_CONFIG.get('app_id')) and
    _AUTH_KEY is not None
)


class OneSignalManager:
    """
    OneSignal Helper Class
    Provides methods for sending push notifications
    """

    ONESIGNAL_API_URL = "https://onesignal.com/api/v1/notifications"

    @staticmethod
    def send_notification_to_all(title, message, url=None, data=None):
        """
        Send notification to all subscribed users

        Args:
            title: Notification title
            message: Notification message body
            url: URL to open when notification is clicked (optional)
            data: Additional data to send with notification (optional)

        Returns:
            dict: API response
        """
        if not ONESIGNAL_ENABLED:
            print(f"OneSignal: Would send notification - Title: {title}, Message: {message}")
            return {'success': False, 'error': 'OneSignal not configured'}

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {_AUTH_KEY}"
        }

        payload = {
            "app_id": ONESIGNAL_CONFIG['app_id'],
            "included_segments": ["All"],
            "headings": {"en": title},
            "contents": {"en": message}
        }

        if url:
            payload["url"] = url

        if data:
            payload["data"] = data

        try:
            response = requests.post(
                OneSignalManager.ONESIGNAL_API_URL,
                headers=headers,
                data=json.dumps(payload)
            )
            return {
                'success': response.status_code == 200,
                'response': response.json()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def send_notification_to_user(player_id, title, message, url=None, data=None):
        """
        Send notification to a specific user

        Args:
            player_id: OneSignal player ID of the user
            title: Notification title
            message: Notification message body
            url: URL to open when notification is clicked (optional)
            data: Additional data to send with notification (optional)

        Returns:
            dict: API response
        """
        if not ONESIGNAL_ENABLED:
            print(f"OneSignal: Would send notification to {player_id} - Title: {title}")
            return {'success': False, 'error': 'OneSignal not configured'}

        if not player_id:
            return {'success': False, 'error': 'Missing OneSignal player ID'}

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {_AUTH_KEY}"
        }

        payload = {
            "app_id": ONESIGNAL_CONFIG['app_id'],
            "include_player_ids": [player_id],
            "headings": {"en": title},
            "contents": {"en": message}
        }

        if url:
            payload["url"] = url

        if data:
            payload["data"] = data

        try:
            response = requests.post(
                OneSignalManager.ONESIGNAL_API_URL,
                headers=headers,
                data=json.dumps(payload)
            )
            return {
                'success': response.status_code == 200,
                'response': response.json()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def send_notification_to_segment(segment, title, message, url=None, data=None):
        """
        Send notification to a specific segment

        Args:
            segment: Segment name (e.g., 'Active Users', 'Inactive Users')
            title: Notification title
            message: Notification message body
            url: URL to open when notification is clicked (optional)
            data: Additional data to send with notification (optional)

        Returns:
            dict: API response
        """
        if not ONESIGNAL_ENABLED:
            print(f"OneSignal: Would send notification to segment '{segment}' - Title: {title}")
            return {'success': False, 'error': 'OneSignal not configured'}

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {_AUTH_KEY}"
        }

        payload = {
            "app_id": ONESIGNAL_CONFIG['app_id'],
            "included_segments": [segment],
            "headings": {"en": title},
            "contents": {"en": message}
        }

        if url:
            payload["url"] = url

        if data:
            payload["data"] = data

        try:
            response = requests.post(
                OneSignalManager.ONESIGNAL_API_URL,
                headers=headers,
                data=json.dumps(payload)
            )
            return {
                'success': response.status_code == 200,
                'response': response.json()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def send_promotional_notification(title, message, discount_code=None):
        """
        Send promotional notification with optional discount code

        Args:
            title: Notification title
            message: Notification message body
            discount_code: Discount code to include (optional)

        Returns:
            dict: API response
        """
        data = {'type': 'promotional'}
        if discount_code:
            data['discount_code'] = discount_code

        return OneSignalManager.send_notification_to_all(
            title=title,
            message=message,
            data=data
        )

    @staticmethod
    def send_booking_confirmation(user_player_id, booking_id, destination_name, travel_date):
        """
        Send booking confirmation notification

        Args:
            user_player_id: OneSignal player ID of the user
            booking_id: Booking ID
            destination_name: Name of the destination
            travel_date: Travel date

        Returns:
            dict: API response
        """
        return OneSignalManager.send_notification_to_user(
            player_id=user_player_id,
            title="Booking Confirmed!",
            message=f"Your trip to {destination_name} on {travel_date} has been confirmed. Booking ID: {booking_id}",
            data={
                'type': 'booking_confirmation',
                'booking_id': booking_id
            }
        )

    @staticmethod
    def send_booking_status_update(user_player_id, booking_id, status, destination_name):
        """
        Send booking status update notification

        Args:
            user_player_id: OneSignal player ID of the user
            booking_id: Booking ID
            status: New booking status
            destination_name: Name of the destination

        Returns:
            dict: API response
        """
        return OneSignalManager.send_notification_to_user(
            player_id=user_player_id,
            title=f"Booking {status}",
            message=f"Your booking for {destination_name} (ID: {booking_id}) has been {status.lower()}.",
            data={
                'type': 'booking_update',
                'booking_id': booking_id,
                'status': status
            }
        )


# JavaScript code for frontend OneSignal integration
_CLIENT_APP_ID = (
    ONESIGNAL_CONFIG.get('app_id')
    if not _is_placeholder(ONESIGNAL_CONFIG.get('app_id'))
    else 'YOUR_ONESIGNAL_APP_ID'
)

ONESIGNAL_CLIENT_SCRIPT = """
<script src="https://cdn.onesignal.com/sdks/OneSignalSDK.js" async=""></script>
<script>
  var OneSignal = window.OneSignal || [];
  OneSignal.push(function() {
    OneSignal.init({
      appId: "__ONESIGNAL_APP_ID__",
    });
  });
</script>
"""
ONESIGNAL_CLIENT_SCRIPT = ONESIGNAL_CLIENT_SCRIPT.replace(
    "__ONESIGNAL_APP_ID__",
    _CLIENT_APP_ID
)

# Instructions for OneSignal Setup:
"""
1. Go to https://onesignal.com/ and create a free account
2. Create a new app and select Web Push
3. Configure your site settings
4. Get your App ID and API keys from Settings > Keys & IDs
5. Replace the placeholder values in ONESIGNAL_CONFIG above
6. Add the ONESIGNAL_CLIENT_SCRIPT to your base template
7. Install requests: pip install requests (already included)
"""
