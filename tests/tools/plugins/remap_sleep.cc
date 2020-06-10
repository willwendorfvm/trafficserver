/*
  Licensed to the Apache Software Foundation (ASF) under one
  or more contributor license agreements.  See the NOTICE file
  distributed with this work for additional information
  regarding copyright ownership.  The ASF licenses this file
  to you under the Apache License, Version 2.0 (the
  "License"); you may not use this file except in compliance
  with the License.  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/

#include <ts/ts.h>
#include <ts/remap.h>

#include <thread>
#include <chrono>
#include <map>
#include <iostream>

//void
//TSPluginInit(int argc, const char *argv[])
//{
//}

///////////////////////////////////////////////////////////////////////////////
// Initialize the plugin as a remap plugin.
//
TSReturnCode
TSRemapInit(TSRemapInterface *api_info, char *errbuf, int errbuf_size)
{
  std::cout << std::endl << "before sleep" << std::endl;
  std::this_thread::sleep_for(std::chrono::seconds(3));
  std::cout << std::endl << "after sleep" << std::endl;
  return TS_SUCCESS; /* success */
}

TSReturnCode
TSRemapNewInstance(int argc, char *argv[], void **ih, char * /* errbuf ATS_UNUSED */, int /* errbuf_size ATS_UNUSED */)
{
  return TS_SUCCESS;
}

void
TSRemapDeleteInstance(void *ih)
{
}

///////////////////////////////////////////////////////////////////////////////
// Main entry point when used as a remap plugin.
//
TSRemapStatus
TSRemapDoRemap(void *ih, TSHttpTxn rh, TSRemapRequestInfo * /* rri ATS_UNUSED */)
{
  return TSREMAP_NO_REMAP;
}
