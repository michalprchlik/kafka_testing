import time
from kafka import KafkaProducer
import logging
from time import sleep
from json import dumps
from kafka.errors import KafkaError
import os

urls = [
	"eam/eam_project_cit_aicv3/(eam)CIT_job49118_time20210719_100852.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job49720_time20210726_102039.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job52226_time20210802_055620.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job52512_time20210802_162609.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job53765_time20210629_102245.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job55260_time20210810_171647.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job55276_time20210811_120349.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job55283_time20210811_125723.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job55296_time20210811_140910.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job55893_time20210827_133858.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job55906_time20210827_145009.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job56558_time20210906_022728.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job56560_time20210906_022828.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job56568_time20210906_033754.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job56570_time20210906_034359.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job56883_time20210916_163036.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job57037_time20210920_110134.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job57041_time20210920_111157.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job58280_time20210927_144804.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job58479_time20210928_134316.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job58968_time20210930_110309.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job59820_time20211005_113135.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job62142_time20210718_184936.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job63078_time20211019_103351.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job66060_time20211102_142207.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job66072_time20211102_145413.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job66094_time20211102_152249.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job66114_time20211102_154018.zip",
"eam/eam_project_cit_aicv3/(eam)CIT_job66963_time20210805_121737.zip",
"eam/eam_project_cit_aicv3_sha/(eam)CIT_job66331_time20210802_113513.zip",
"eam/eam_project_cit_aicv3_sha/(eam)CIT_job66956_time20210805_115203.zip",
"eam/eam_project_ilmt_aicv3/(eam)CIT_job49902_time20210727_134442.zip",
"eam/eam_project_ilmt_aicv3/(eam)CIT_job50031_time20210728_111512.zip",
"eam/eam_project_ilmt_aicv3/(eam)CIT_job50738_time20210730_172427.zip",
"eam/eam_project_ilmt_aicv3/(eam)CIT_job52980_time20210803_103509.zip",
"eam/eam_project_ilmt_aicv3/(eam)CIT_job55454_time20210817_042837.zip",
"eam/kyn_project_cit_aic_sha/(eam)CIT_job61837_time20211208_025556.zip",
"eam/kyn_project_cit_aic_sha/(eam)CIT_job61839_time20211208_025746.zip",
"eam/kyn_project_cit_aic_sha/(eam)CIT_job68555_time20211118_011937.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job58811_time20210929_233308.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job58813_time20210929_233945.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job58823_time20210930_001107.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job59149_time20211001_011751.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job59157_time20211001_020450.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job59905_time20211005_154443.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job59915_time20211005_162607.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job60829_time20211008_160317.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job60831_time20211008_160928.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job61807_time20211208_020630.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job61813_time20211208_021147.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job62232_time20211014_171030.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job62953_time20211019_003039.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job62977_time20211019_020506.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job63700_time20211022_101001.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job67331_time20211110_023312.zip",
"eam/kyn_project_ilmt_aic_sha/(eam)CIT_job67333_time20211110_024006.zip",
]

urls = [
	"eam/eam_project_cit_aicv3/(eam)CIT_job66060_time20211102_142207.zip"
]

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s %(levelname)s %(message)s',
	datefmt='%H:%M:%S'
)

logging.info("@@@@@@@@@@@@@@@@@@@@@@@@@@")

producer = KafkaProducer(bootstrap_servers=['localhost:9094'],
						 value_serializer=lambda x: 
						 dumps(x).encode('utf-8'))
offset = 1
for url in urls:
	value = f"{offset} - {url}"
	logging.info(f"producer, url={value}")
	name = os.path.basename(url)
	data = {'path' : url, 'name': name}
	producer.send('sfs_scan_files', value=data)
	offset = offset + 1
	sleep(1)

