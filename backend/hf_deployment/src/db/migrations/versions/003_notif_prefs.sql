-- Migration 003: Create NotificationPreference Table
-- Feature: 012-advanced-todo-features
-- Date: 2026-02-05
-- Purpose: Per-user notification settings and permission status

CREATE TABLE notification_preferences (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    notification_enabled BOOLEAN DEFAULT TRUE,
    reminder_minutes_before INTEGER DEFAULT 15 CHECK (reminder_minutes_before >= 0 AND reminder_minutes_before <= 1440),
    browser_permission_granted BOOLEAN DEFAULT FALSE,
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for enabled notifications
CREATE INDEX idx_notif_pref_enabled ON notification_preferences(user_id, notification_enabled)
WHERE notification_enabled = TRUE;

-- Comments for documentation
COMMENT ON TABLE notification_preferences IS 'Per-user notification settings and browser permission status';
COMMENT ON COLUMN notification_preferences.notification_enabled IS 'Global notification toggle (on/off)';
COMMENT ON COLUMN notification_preferences.reminder_minutes_before IS 'Default reminder time in minutes (0-1440)';
COMMENT ON COLUMN notification_preferences.browser_permission_granted IS 'Whether browser Notification API permission granted';
COMMENT ON COLUMN notification_preferences.timezone IS 'User timezone for display (informational, not used for storage)';
