'''
'''
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import os

Test.Summary = '''
Test duplicate command: traffic_ctl config reload (YTSATS-3294)
'''
Test.testName = 'Duplicate Reload Test'

ts = Test.MakeATSProcess("ts", command="traffic_manager", select_ports=True)

ts.Disk.records_config.update({
    'proxy.config.diags.debug.enabled': 0,
})

# Add dummy remap rule
ts.Disk.remap_config.AddLine(
    'map http://1.example http://1.other @plugin=remap_sleep.so'
)

# Load plugin
Test.PreparePlugin(os.path.join(Test.Variables.AtsTestToolsDir, 'plugins', 'remap_sleep.cc'),
        ts, add_plugin_config=False)

#
# Test body
#

# t = Test.AddTestRun("Test traffic server started properly")
# t.StillRunningAfter = Test.Processes.ts
# p = t.Processes.Default
# p.Command = "curl http://127.0.0.1:{0}".format(ts.Variables.port)
# p.ReturnCode = 0 
# p.StartBefore(Test.Processes.ts)

# First reload
tr = Test.AddTestRun("Original reload config")
tr.Processes.Default.StartBefore(Test.Processes.ts, ready=When.PortReady(ts.Variables.port))
tr.Processes.Default.Command = 'traffic_ctl config reload'
# Need to copy over the environment so traffic_ctl knows where to find the unix domain socket
tr.Processes.Default.Env = ts.Env
tr.Processes.Default.ReturnCode = 0
tr.Processes.Default.TimeOut = 5
tr.TimeOut = 5
tr.StillRunningAfter = ts

# Second reload
tr = Test.AddTestRun("Duplicate reload config")
tr.Processes.Default.Command = 'traffic_ctl config reload'
# Need to copy over the environment so traffic_ctl knows where to find the unix domain socket
tr.Processes.Default.Env = ts.Env
tr.Processes.Default.ReturnCode = 0
tr.Processes.Default.TimeOut = 5
tr.TimeOut = 5
tr.StillRunningAfter = ts
