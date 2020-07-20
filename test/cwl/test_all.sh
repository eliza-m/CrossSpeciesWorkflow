

cwltool --no-match-user --no-read-only --debug ${CSW_HOME}/cwl/phosphorylation/netphospan.cwl yml/netphospan_generic.yml
cwltool --no-match-user --no-read-only --debug ${CSW_HOME}/cwl/phosphorylation/netphospan.cwl yml/netphospan_kinase.yml

cwltool --no-match-user --no-read-only --debug ${CSW_HOME}/cwl/phosphorylation/netphos.cwl yml/netphos.yml

cwltool --no-match-user --no-read-only --debug ${CSW_HOME}/cwl/structural/scratch1d.cwl yml/scratch1d.yml




