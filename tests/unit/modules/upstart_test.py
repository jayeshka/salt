# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Jayesh Kariya <jayeshk@saltstack.com>`
'''
# Import Python Libs
from __future__ import absolute_import

# Import Salt Testing Libs
from salttesting import TestCase, skipIf
from salttesting.mock import (
    MagicMock,
    patch,
    NO_MOCK,
    NO_MOCK_REASON
)
from salttesting.helpers import ensure_in_syspath

ensure_in_syspath('../../')

# Import Salt Libs
from salt.modules import upstart

# Globals
upstart.__salt__ = {}


@skipIf(NO_MOCK, NO_MOCK_REASON)
class UpstartTestCase(TestCase):
    '''
    Test cases for salt.modules.lvs
    '''
    def test_get_enabled(self):
        '''
        Test to return the enabled services
        '''
        service_names = ['A']

        with patch.object(upstart, '_iter_service_names',
                          return_value=service_names):
            with patch.object(upstart, '_service_is_upstart',
                              side_effect=[True, False]):

                with patch.object(upstart, '_upstart_is_enabled',
                                  return_value=True):
                    self.assertListEqual(upstart.get_enabled(), service_names)

                with patch.object(upstart, '_service_is_sysv',
                                  return_value=True):
                    with patch.object(upstart, '_sysv_is_enabled',
                                      return_value=True):
                        self.assertListEqual(upstart.get_enabled(),
                                             service_names)

    def test_get_disabled(self):
        '''
        Test to return the disabled services
        '''
        service_names = ['A']

        with patch.object(upstart, '_iter_service_names',
                          return_value=service_names):
            with patch.object(upstart, '_service_is_upstart',
                              side_effect=[True, False]):

                with patch.object(upstart, '_upstart_is_disabled',
                                  return_value=True):
                    self.assertListEqual(upstart.get_disabled(), service_names)

                with patch.object(upstart, '_service_is_sysv',
                                  return_value=True):
                    with patch.object(upstart, '_sysv_is_disabled',
                                      return_value=True):
                        self.assertListEqual(upstart.get_disabled(),
                                             service_names)

    def test_available(self):
        '''
        Test to returns ``True`` if the specified service is available,
        otherwise returns ``False``.
        '''
        service_names = ['A']
        with patch.object(upstart, 'get_all', return_value=service_names):
            self.assertTrue(upstart.missing('B'))
            self.assertFalse(upstart.missing('A'))

    def test_missing(self):
        '''
        Test to returns ``True`` if the specified service is not available,
        otherwise returns ``False``.
        '''
        service_names = ['A']
        with patch.object(upstart, 'get_all', return_value=service_names):
            self.assertTrue(upstart.missing('B'))
            self.assertFalse(upstart.missing('A'))

    def test_get_all(self):
        '''
        Test to return all installed services
        '''
        with patch.object(upstart, 'get_enabled', return_value=['A']):
            with patch.object(upstart, 'get_disabled', return_value=['B']):
                self.assertListEqual(upstart.get_all(), ['A', 'B'])

    def test_start(self):
        '''
        Test to start the specified service
        '''
        mock = MagicMock(return_value=True)
        with patch.dict(upstart.__salt__, {'cmd.retcode': mock}):
            self.assertFalse(upstart.start('A'))

    def test_stop(self):
        '''
        Test to stop the specified service
        '''
        mock = MagicMock(return_value=True)
        with patch.dict(upstart.__salt__, {'cmd.retcode': mock}):
            self.assertFalse(upstart.stop('A'))

    def test_restart(self):
        '''
        Test to restart the named service
        '''
        mock = MagicMock(return_value=True)
        with patch.dict(upstart.__salt__, {'cmd.retcode': mock}):
            self.assertFalse(upstart.restart('A'))

    def test_full_restart(self):
        '''
        Test to do a full restart (stop/start) of the named service
        '''
        mock = MagicMock(return_value=True)
        with patch.dict(upstart.__salt__, {'cmd.retcode': mock}):
            self.assertFalse(upstart.full_restart('A'))

    def test_reload_(self):
        '''
        Test to reload the named service
        '''
        mock = MagicMock(return_value=True)
        with patch.dict(upstart.__salt__, {'cmd.retcode': mock}):
            self.assertFalse(upstart.reload_('A'))

    def test_force_reload(self):
        '''
        Test to force-reload the named service
        '''
        mock = MagicMock(return_value=True)
        with patch.dict(upstart.__salt__, {'cmd.retcode': mock}):
            self.assertFalse(upstart.force_reload('A'))

    def test_status(self):
        '''
        Test to return the status for a service, returns a bool whether
        the service is running.
        '''
        mock = MagicMock(return_value=True)
        with patch.dict(upstart.__salt__, {'status.pid': mock}):
            self.assertTrue(upstart.status('A', 1))

        with patch.object(upstart, '_service_is_upstart', return_value=True):
            mock = MagicMock(return_value=[1])
            with patch.dict(upstart.__salt__, {'cmd.run': mock}):
                self.assertFalse(upstart.status('A'))

        with patch.dict(upstart.__salt__, {'cmd.retcode': mock}):
            self.assertFalse(upstart.status('A'))

    def test_enable(self):
        '''
        Test to enable the named service to start at boot
        '''
        with patch.object(upstart, '_service_is_upstart',
                          side_effect=[True, False]):
            self.assertTrue(upstart.enable('A'))

            with patch.object(upstart, '_get_service_exec', return_value='A'):
                mock = MagicMock(return_value=[1])
                with patch.dict(upstart.__salt__, {'cmd.retcode': mock}):
                    self.assertFalse(upstart.enable('A'))

    def test_disable(self):
        '''
        Test to disable the named service from starting on boot
        '''
        with patch.object(upstart, '_service_is_upstart',
                          side_effect=[True, False]):
            with patch.object(upstart, '_upstart_disable', return_value=True):
                self.assertTrue(upstart.disable('A'))

            with patch.object(upstart, '_get_service_exec', return_value='A'):
                mock = MagicMock(return_value=[1])
                with patch.dict(upstart.__salt__, {'cmd.retcode': mock}):
                    self.assertFalse(upstart.disable('A'))

    def test_enabled(self):
        '''
        Test to check to see if the named service is enabled to start on boot
        '''
        with patch.object(upstart, '_service_is_upstart',
                          side_effect=[True, False, False]):
            with patch.object(upstart, '_upstart_is_enabled',
                              return_value=True):
                self.assertTrue(upstart.enabled('A'))

            with patch.object(upstart, '_service_is_sysv',
                              side_effect=[True, False]):
                with patch.object(upstart, '_sysv_is_enabled',
                                  return_value=True):
                    self.assertTrue(upstart.enabled('A'))

                    self.assertIsNone(upstart.enabled('A'))

    def test_disabled(self):
        '''
        Test to check to see if the named service is disabled to start on boot
        '''
        with patch.object(upstart, '_service_is_upstart',
                          side_effect=[True, False, False]):
            with patch.object(upstart, '_upstart_is_disabled',
                              return_value=False):
                self.assertTrue(upstart.enabled('A'))

            with patch.object(upstart, '_service_is_sysv',
                              side_effect=[True, False]):
                with patch.object(upstart, '_sysv_is_disabled',
                                  return_value=False):
                    self.assertTrue(upstart.enabled('A'))

                    self.assertIsNone(upstart.enabled('A'))

if __name__ == '__main__':
    from integration import run_tests
    run_tests(UpstartTestCase, needs_daemon=False)
