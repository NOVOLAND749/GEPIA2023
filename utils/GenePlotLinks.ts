import GeneDetailType from "~/types/GeneDetailType";
import { SynthUrl } from "./SynthUrl";

export function getGenePlotLinks(gene: GeneDetailType) {
  return {
    StripPlot: SynthUrl(["getStripPlot"], { gene: gene.gene_name }),
    BarPlot: SynthUrl(["getBarPlot"], { gene: gene.gene_name }),
    CopyNumberPlot: SynthUrl(["getCopyNumberPlot"], { gene: gene.gene_name }),
  };
}
