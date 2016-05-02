package macrobase.analysis.classify;

import macrobase.analysis.pipeline.operator.MBStream;
import macrobase.analysis.result.OutlierClassificationResult;
import macrobase.analysis.stats.mixture.BatchMixtureModel;
import macrobase.conf.ConfigurationException;
import macrobase.conf.MacroBaseConf;
import macrobase.datamodel.Datum;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class MixtureGroupClassifier implements OutlierClassifier {
    private static final Logger log = LoggerFactory.getLogger(MixtureGroupClassifier.class);
    private final List<Double> targetGroup;

    MBStream<OutlierClassificationResult> results = new MBStream<>();

    public MixtureGroupClassifier(MacroBaseConf conf, BatchMixtureModel mixtureModel) throws ConfigurationException {
        this.targetGroup = conf.getDoubleList(MacroBaseConf.TARGET_GROUP);
    }

    @Override
    public void initialize() throws Exception {

    }

    @Override
    public void consume(List<Datum> records) throws Exception {

    }

    @Override
    public void shutdown() throws Exception {

    }

    @Override
    public MBStream<OutlierClassificationResult> getStream() throws Exception {
        return null;
    }
}
