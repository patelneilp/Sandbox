import { useState } from "react";
import { parseEntityInput } from "../utils/entity-parser";

interface Props {
  onSubmit: (entities: string[]) => Promise<void>;
}

export const EntityUploader = ({ onSubmit }: Props) => {
  const [input, setInput] = useState("");

  return (
    <section>
      <h2>Upload chemical entities</h2>
      <textarea
        rows={8}
        value={input}
        placeholder="Enter SMILES, InChI, ChEMBL IDs, or CAS values separated by commas/new lines"
        onChange={(event) => setInput(event.target.value)}
      />
      <button onClick={() => onSubmit(parseEntityInput(input))}>Analyze</button>
    </section>
  );
};
