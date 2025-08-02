"""HTPI Dashboard Service - Provides dashboard statistics and metrics"""

import os
import asyncio
import json
import logging
from datetime import datetime, timedelta
import nats
from nats.aio.client import Client as NATS
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
NATS_URL = os.environ.get('NATS_URL', 'nats://localhost:4222')

class DashboardService:
    def __init__(self):
        self.nc = None
        
    async def connect(self):
        """Connect to NATS"""
        try:
            self.nc = await nats.connect(NATS_URL)
            logger.info(f"Connected to NATS at {NATS_URL}")
            
            # Subscribe to dashboard requests
            await self.nc.subscribe("htpi.dashboard.get.stats", cb=self.handle_get_stats)
            await self.nc.subscribe("htpi.dashboard.get.activity", cb=self.handle_get_activity)
            await self.nc.subscribe("htpi.dashboard.get.alerts", cb=self.handle_get_alerts)
            
            logger.info("Dashboard service subscriptions established")
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {str(e)}")
            raise
    
    async def handle_get_stats(self, msg):
        """Handle dashboard statistics request"""
        try:
            data = json.loads(msg.data.decode())
            tenant_id = data.get('tenantId')
            client_id = data.get('clientId')
            portal = data.get('portal', 'customer')
            
            # Generate mock statistics (in production, would query MongoDB)
            stats = {
                'patients': {
                    'total': random.randint(150, 250),
                    'new_this_month': random.randint(10, 30),
                    'active': random.randint(100, 200)
                },
                'claims': {
                    'total': random.randint(400, 600),
                    'pending': random.randint(20, 50),
                    'approved': random.randint(300, 500),
                    'denied': random.randint(10, 30),
                    'total_amount': f"${random.randint(50000, 150000):,}"
                },
                'encounters': {
                    'today': random.randint(10, 25),
                    'this_week': random.randint(50, 100),
                    'this_month': random.randint(200, 400)
                },
                'insurance': {
                    'verified': random.randint(100, 180),
                    'pending_verification': random.randint(10, 30),
                    'expired': random.randint(5, 15)
                }
            }
            
            # Send response
            channel = f"{portal}.dashboard.response.{client_id}"
            await self.nc.publish(channel, 
                json.dumps({
                    'success': True,
                    'stats': stats,
                    'tenantId': tenant_id,
                    'clientId': client_id,
                    'timestamp': datetime.utcnow().isoformat()
                }).encode())
            
            logger.info(f"Sent dashboard stats for tenant {tenant_id}")
            
        except Exception as e:
            logger.error(f"Error in handle_get_stats: {str(e)}")
    
    async def handle_get_activity(self, msg):
        """Handle recent activity request"""
        try:
            data = json.loads(msg.data.decode())
            tenant_id = data.get('tenantId')
            client_id = data.get('clientId')
            portal = data.get('portal', 'customer')
            
            # Generate mock activity (in production, would query MongoDB)
            activities = []
            activity_types = [
                ('patient_added', 'New patient registered'),
                ('claim_submitted', 'Claim submitted to insurance'),
                ('payment_received', 'Payment received'),
                ('appointment_scheduled', 'Appointment scheduled'),
                ('insurance_verified', 'Insurance verified')
            ]
            
            for i in range(10):
                activity_type, description = random.choice(activity_types)
                activities.append({
                    'id': f'activity-{i+1}',
                    'type': activity_type,
                    'description': description,
                    'timestamp': (datetime.utcnow() - timedelta(hours=i*2)).isoformat(),
                    'user': f'user{random.randint(1, 5)}@example.com'
                })
            
            # Send response
            channel = f"{portal}.dashboard.response.{client_id}"
            await self.nc.publish(channel, 
                json.dumps({
                    'success': True,
                    'activities': activities,
                    'tenantId': tenant_id,
                    'clientId': client_id
                }).encode())
            
        except Exception as e:
            logger.error(f"Error in handle_get_activity: {str(e)}")
    
    async def handle_get_alerts(self, msg):
        """Handle alerts/notifications request"""
        try:
            data = json.loads(msg.data.decode())
            tenant_id = data.get('tenantId')
            client_id = data.get('clientId')
            portal = data.get('portal', 'customer')
            
            # Generate mock alerts
            alerts = [
                {
                    'id': 'alert-1',
                    'type': 'warning',
                    'title': 'Insurance Verifications Pending',
                    'message': '12 patients have insurance pending verification',
                    'timestamp': datetime.utcnow().isoformat()
                },
                {
                    'id': 'alert-2',
                    'type': 'info',
                    'title': 'Monthly Report Available',
                    'message': 'Your July 2024 financial report is ready',
                    'timestamp': (datetime.utcnow() - timedelta(hours=2)).isoformat()
                },
                {
                    'id': 'alert-3',
                    'type': 'success',
                    'title': 'Claims Batch Processed',
                    'message': '45 claims successfully submitted to insurers',
                    'timestamp': (datetime.utcnow() - timedelta(hours=5)).isoformat()
                }
            ]
            
            # Send response
            channel = f"{portal}.dashboard.response.{client_id}"
            await self.nc.publish(channel, 
                json.dumps({
                    'success': True,
                    'alerts': alerts,
                    'tenantId': tenant_id,
                    'clientId': client_id
                }).encode())
            
        except Exception as e:
            logger.error(f"Error in handle_get_alerts: {str(e)}")
    
    async def simulate_real_time_updates(self):
        """Simulate real-time dashboard updates"""
        while True:
            try:
                await asyncio.sleep(30)  # Update every 30 seconds
                
                # Simulate update for each tenant
                tenants = ['tenant-001', 'tenant-002']
                
                for tenant_id in tenants:
                    # Generate random update
                    update_types = [
                        {
                            'type': 'patient_update',
                            'data': {
                                'action': 'new_patient',
                                'count': 1,
                                'patient_name': f'Patient {random.randint(1000, 9999)}'
                            }
                        },
                        {
                            'type': 'claim_update',
                            'data': {
                                'action': 'claim_approved',
                                'claim_id': f'CLM-{random.randint(1000, 9999)}',
                                'amount': f'${random.randint(100, 1000)}'
                            }
                        },
                        {
                            'type': 'encounter_update',
                            'data': {
                                'action': 'encounter_completed',
                                'provider': f'Dr. {random.choice(["Smith", "Johnson", "Williams"])}'
                            }
                        }
                    ]
                    
                    update = random.choice(update_types)
                    update['timestamp'] = datetime.utcnow().isoformat()
                    update['tenantId'] = tenant_id
                    
                    # Broadcast to both portals
                    for portal in ['admin', 'customer']:
                        await self.nc.publish(f"{portal}.broadcast.dashboard.{tenant_id}", 
                            json.dumps(update).encode())
                    
                    logger.info(f"Sent dashboard update for tenant {tenant_id}")
                    
            except Exception as e:
                logger.error(f"Error in simulate_real_time_updates: {str(e)}")
    
    async def run(self):
        """Run the service"""
        await self.connect()
        logger.info("Dashboard service is running...")
        
        # Start real-time update simulation
        asyncio.create_task(self.simulate_real_time_updates())
        
        # Keep service running
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            pass
        finally:
            await self.nc.close()

async def main():
    """Main entry point"""
    service = DashboardService()
    await service.run()

if __name__ == '__main__':
    asyncio.run(main())