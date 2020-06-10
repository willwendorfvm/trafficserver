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
tr = Test.AddTestRun("Original and duplicated reload config")
tr.Env = ts.Env
tr.TimeOut = 5
tr.StillRunningAfter = ts

lst = []
lst.append(tr.Processes.Process(
        name="touch-{num}".format(num=0),
        cmdstr = "touch {file}".format(file=os.path.join(tr.RunDirectory, 'ts/config/remap.config')),
        returncode = 0
    )
)
lst.append(tr.Processes.Process(
        name="reload-{num}".format(num=1),
        cmdstr = "traffic_ctl config reload",
        returncode = 0
    )
)
lst.append(tr.Processes.Process(
        name="touch-{num}".format(num=2),
        cmdstr = "touch {file}".format(file=os.path.join(tr.RunDirectory, 'ts/config/remap.config')),
        returncode = 0
    )
)
lst.append(tr.Processes.Process(
        name="reload-{num}".format(num=3),
        cmdstr = "traffic_ctl config reload",
        returncode = 0
    )
)
lst[0].StartBefore(Test.Processes.ts, ready=When.FileExists(os.path.join(tr.RunDirectory, 'ts/log/diags.log')))
lst[1].StartBefore(tr.Processes.touch-0)
lst[2].StartBefore(tr.Processes.reload-1)
lst[3].StartBefore(tr.Processes.touch-2)
