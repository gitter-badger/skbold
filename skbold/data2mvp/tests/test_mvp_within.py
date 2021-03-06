from skbold.data2mvp import MvpWithin
from skbold import testdata_path
import os
import os.path as op
import pytest

gm_mask = op.join(op.dirname(op.dirname(op.dirname(__file__))), 'data', 'ROIs',
                  'GrayMatter.nii.gz')

@pytest.mark.parametrize('ref_space', ['mni', 'epi'])
@pytest.mark.parametrize('mask', [None, gm_mask])
def test_fsl2mvp_within(ref_space, mask):

    testfeats = [op.join(testdata_path, 'run1.feat'),
                 op.join(testdata_path, 'run2.feat')]

    true_labels = ['actie', 'actie', 'actie',
                   'interoception', 'interoception', 'interoception',
                   'situation', 'situation', 'situation']

    mvp_within = MvpWithin(source=testfeats, read_labels=True,
                           remove_contrast=[], invert_selection=None,
                           ref_space=ref_space, beta2tstat=True,
                           remove_zeros=False, mask=mask)

    mvp_within.create()
    assert len(mvp_within.contrast_labels) == 2 * len(true_labels)

    fn = op.dirname(testfeats[0])
    mvp_within.write(path=fn, backend='joblib')
    assert op.isfile(op.join(fn, 'mvp.jl'))
    os.remove(op.join(fn, 'mvp.jl'))
