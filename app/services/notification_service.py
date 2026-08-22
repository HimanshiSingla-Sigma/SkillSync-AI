from app.core.logging import logger


class NotificationService:
    """Handles operational alerts, placement notifications, and transactional logs."""

    @staticmethod
    async def notify_application_status_update(
        student_email: str,
        student_name: str,
        company_name: str,
        drive_title: str,
        new_status: str,
        remarks: str = "",
    ) -> None:
        """Sends or logs real-time status update notifications."""
        logger.info(
            f"[NOTIFICATION] Status Update Alert sent to '{student_email}' ({student_name}): "
            f"Your application for '{drive_title}' at '{company_name}' has moved to '{new_status}'. "
            f"Remarks: '{remarks}'"
        )

    @staticmethod
    async def notify_drive_published(
        company_name: str,
        drive_title: str,
        target_programmes: list,
    ) -> None:
        """Broadcasts new placement drive alerts."""
        logger.info(
            f"[NOTIFICATION] New Placement Drive Broadcast: '{company_name}' posted '{drive_title}' "
            f"for programmes: {target_programmes}."
        )