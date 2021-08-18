# SPDX-FileCopyrightText: 2022 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0
import glob
import os

import ttfw_idf
from tiny_test_fw import Utility


@ttfw_idf.idf_component_unit_test(env_tag='COMPONENT_UT_GENERIC', target=['esp32', 'esp32s2', 'esp32s3', 'esp32c3'])
def test_component_ut_i2s(env, _):  # type: (ttfw_idf.TinyFW.Env, None) -> None
    # Get the names of all configs (sdkconfig.ci.* files)
    config_files = glob.glob(os.path.join(os.path.dirname(__file__), 'sdkconfig.ci.*'))
    config_names = [os.path.basename(s).replace('sdkconfig.ci.', '') for s in config_files]

    # Run test once with binaries built for each config
    for name in config_names:
        Utility.console_log(f'Checking config "{name}"... ', end='')
        dut = env.get_dut('i2s', 'components/driver/test_apps/i2s', app_config_name=name)
        dut.start_app()
        stdout = dut.expect('Press ENTER to see the list of tests', full_stdout=True)
        dut.write('*')
        stdout = dut.expect("Enter next test, or 'enter' to see menu", full_stdout=True, timeout=30)
        ttfw_idf.ComponentUTResult.parse_result(stdout,ttfw_idf.TestFormat.UNITY_BASIC)
        env.close_dut(dut.name)
        Utility.console_log(f'Test config "{name}" done')


if __name__ == '__main__':
    test_component_ut_i2s()
